import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "q1.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS progression (
        cours_id TEXT PRIMARY KEY,
        progression INTEGER DEFAULT 0,
        termine INTEGER DEFAULT 0
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS quiz_scores (
        quiz_id TEXT PRIMARY KEY,
        score INTEGER DEFAULT 0,
        total INTEGER DEFAULT 0
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS user (
        id INTEGER PRIMARY KEY,
        premium INTEGER DEFAULT 0
    )""")
    c.execute("INSERT OR IGNORE INTO user (id, premium) VALUES (1, 0)")
    conn.commit()
    conn.close()

def is_premium():
    conn = sqlite3.connect(DB_PATH)
    r = conn.execute("SELECT premium FROM user WHERE id=1").fetchone()
    conn.close()
    return bool(r and r[0])

def set_premium(val):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("UPDATE user SET premium=? WHERE id=1", (1 if val else 0,))
    conn.commit()
    conn.close()

def get_progression(cours_id):
    conn = sqlite3.connect(DB_PATH)
    r = conn.execute("SELECT progression FROM progression WHERE cours_id=?", (cours_id,)).fetchone()
    conn.close()
    return r[0] if r else 0

def set_progression(cours_id, prog):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""INSERT INTO progression (cours_id, progression) VALUES (?, ?)
                    ON CONFLICT(cours_id) DO UPDATE SET progression=?""", (cours_id, prog, prog))
    conn.commit()
    conn.close()
