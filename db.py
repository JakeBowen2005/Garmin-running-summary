import sqlite3

DB_PATH = "garmin_data.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE
        );
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS activities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            date TEXT,
            week INTEGER,
            weekday TEXT,
            month TEXT,
            distance REAL,
            avg_pace REAL,
            time REAL,
            avg_hr REAL,
            max_hr REAL,
            best_pace REAL,
            zones TEXT,
            ascent REAL,
            descent REAL,
            steps INTEGER,
            calories REAL,
            distance_range TEXT,
            UNIQUE(user_id, date, time),
            FOREIGN KEY(user_id) REFERENCES users(id)
        );
    """)
    conn.commit()
    conn.close()


def insert_activity(user_id, row):
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            INSERT INTO activities (
                user_id, date, week, weekday, month, distance, avg_pace,
                time, avg_hr, max_hr, best_pace, zones, ascent, descent,
                steps, calories, distance_range
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, (user_id, *row))
        conn.commit()

    except sqlite3.IntegrityError:
        # duplicate → safely ignore
        pass

    finally:
        conn.close()

def get_or_create_user(email: str) -> int:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id FROM users WHERE email = ?;", (email,))
    row = cur.fetchone()
    if row is not None:
        conn.close()
        return int(row[0])
    cur.execute("INSERT INTO users (email) VALUES (?);", (email,))
    conn.commit()
    user_id = int(cur.lastrowid)
    conn.close()
    return user_id
