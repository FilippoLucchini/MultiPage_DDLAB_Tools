import sqlite3
import datetime

DB_FILE = "lab_data.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    # Samples table
    c.execute('''
        CREATE TABLE IF NOT EXISTS samples (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,
            date TEXT NOT NULL
        )
    ''')

    # Runs table
    c.execute('''
        CREATE TABLE IF NOT EXISTS runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            platform TEXT NOT NULL,
            date TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()


def add_sample(sample_type, date):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO samples (type, date) VALUES (?, ?)", 
              (sample_type, date.isoformat()))
    conn.commit()
    conn.close()


def add_run(platform, date):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO runs (platform, date) VALUES (?, ?)", 
              (platform, date.isoformat()))
    conn.commit()
    conn.close()


def get_samples(year=None):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    if year:
        start = f"{year}-01-01"
        end = f"{year}-12-31"
        c.execute("SELECT type, date FROM samples WHERE date BETWEEN ? AND ?", (start, end))
    else:
        c.execute("SELECT type, date FROM samples")
    rows = c.fetchall()
    conn.close()
    return [{"type": r[0], "date": datetime.date.fromisoformat(r[1])} for r in rows]


def get_runs(year=None):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    if year:
        start = f"{year}-01-01"
        end = f"{year}-12-31"
        c.execute("SELECT platform, date FROM runs WHERE date BETWEEN ? AND ?", (start, end))
    else:
        c.execute("SELECT platform, date FROM runs")
    rows = c.fetchall()
    conn.close()
    return [{"platform": r[0], "date": datetime.date.fromisoformat(r[1])} for r in rows]
