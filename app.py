from flask import Flask, render_template, request
from datetime import datetime
from database import connect_db, create_table

app = Flask(__name__)

create_table()

def calculate_age(civil_id):
    if len(civil_id) != 12 or not civil_id.isdigit():
        return None

    if civil_id[0] == "2":
        birth_year = int("19" + civil_id[1:3])
    elif civil_id[0] == "3":
        birth_year = int("20" + civil_id[1:3])
    else:
        return None

    return datetime.now().year - birth_year

def check_daily_limit(civil_id, product):
    conn = connect_db()
    cursor = conn.cursor()
    today = datetime.now().strftime("%Y-%m-%d")

    cursor.execute(
        "SELECT COUNT(*) FROM purchases WHERE civil_id=%s AND product=%s AND date=%s",
        (civil_id, product, today)
    )

    count = cursor.fetchone()[0]
    conn.close()
    return count < 1

def save_purchase(civil_id, product):
    conn = connect_db()
    cursor = conn.cursor()
    today = datetime.now().strftime("%Y-%m-%d")

    cursor.execute(
        "INSERT INTO purchases (civil_id, product, date) VALUES (%s, %s, %s)",
        (civil_id, product, today)
    )

    conn.commit()
    conn.close()

@app.route("/", methods=["GET", "POST"])
def home():
    result = ""
    status = ""
    age = ""

    if request.method == "POST":
        civil_id = request.form["civil_id"]
        product = request.form["product"]

        age = calculate_age(civil_id)

        if age is None:
            result = "Invalid Civil ID"
            status = "blocked"
        elif product == "nicotine" and age < 21:
            result = "Blocked: Underage for nicotine"
            status = "blocked"
        elif product == "energy" and age < 16:
            result = "Blocked: Underage for energy drinks"
            status = "blocked"
        elif not check_daily_limit(civil_id, product):
            result = "Blocked: Daily limit reached"
            status = "blocked"
        else:
            save_purchase(civil_id, product)
            result = "Approved: Purchase allowed"
            status = "approved"

    return render_template("index.html", result=result, status=status, age=age)

if __name__ == "__main__":
    app.run(debug=True)