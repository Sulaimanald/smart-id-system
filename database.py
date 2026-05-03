import os
import sqlite3
import psycopg2

DATABASE_URL = os.environ.get("DATABASE_URL")

def connect_db():
    if DATABASE_URL:
        return psycopg2.connect(DATABASE_URL)
    else:
        return sqlite3.connect("system.db")

def create_table():
    conn = connect_db()
    cursor = conn.cursor()

    if DATABASE_URL:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS purchases (
            id SERIAL PRIMARY KEY,
            civil_id TEXT NOT NULL,
            product TEXT NOT NULL,
            date TEXT NOT NULL
        )
        """)
    else:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS purchases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            civil_id TEXT NOT NULL,
            product TEXT NOT NULL,
            date TEXT NOT NULL
        )
        """)

    conn.commit()
    conn.close()