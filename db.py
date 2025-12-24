import sqlite3

DB_PATH = "garmin_data.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS activities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
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
            calories INTEGER,
            distance_range TEXT,
            UNIQUE(date, time)
        );
    """)
    conn.commit()
    conn.close()


def insert_activity(row):
    conn = get_connection()
    curr = conn.cursor()

    try:
        curr.execute("""
            INSERT INTO activities (
                date, week, weekday, month, distance, avg_pace,
                time, avg_hr, max_hr, best_pace, zones, ascent, descent,
                steps, calories, distance_range
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, tuple(row))
        conn.commit()

    except sqlite3.IntegrityError:
        pass
    finally:
        conn.close()
