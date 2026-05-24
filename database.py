import sqlite3
from datetime import datetime

DB_PATH = "baby.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS records(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT,
            time TEXT,
            memo TEXT DEFAULT ''
        )
    """)
    conn.commit()
    conn.close()

def add_record(category: str, memo: str ="") -> None:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    now = datetime.now().strftime("%m/%d %H:%M")
    cursor.execute(
        "INSERT INTO records (category, time, memo) VALUES (?, ?, ?)",
        (category, now, memo)
    )
    conn.commit()
    conn.close()

def get_record() -> list:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, category, time FROM records ORDER BY id DESC")
    records = cursor.fetchall()
    conn.close()
    return records

def delete_record(record_id: int) -> None:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM records WHERE id = ?", (record_id,))
    conn.commit()
    conn.close()

def get_count_by_date(category: str, date_str: str) -> int:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT COUNT(*) FROM records WHERE category = ? AND time LIKE ? ",
        (category, f"{date_str}%")
    )
    count = cursor.fetchone()[0]
    conn.close()
    return count

def get_records_by_date(date_str: str) -> list:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, category, time, memo FROM records WHERE time LIKE ? ORDER BY id DESC",
        (f"{date_str}%",)
    )
    records = cursor.fetchall()
    conn.close()
    return records

def get_sleep_time(date_str: str) -> str:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 入眠と起床を時間順に取得
    cursor.execute(
        "SELECT category, time FROM records WHERE category IN ('入眠', '起床') AND time LIKE ? ORDER BY id",
        (f"{date_str}%",)
    )
    records = cursor.fetchall()
    conn.close()

    total_minutes = 0
    last_sleep = None

    for category, time in records:
        if category == "入眠":
            last_sleep = time
        elif category == "起床" and last_sleep is not None:
            # 入眠時刻と起床時刻から差分を計算
            sleep_time = datetime.strptime(last_sleep, "%m/%d %H:%M")
            wake_time = datetime.strptime(time, "%m/%d %H:%M")
            diff = (wake_time - sleep_time).total_seconds() / 60
            total_minutes += diff
            last_sleep = None

    hours = int(total_minutes // 60)
    minutes = int(total_minutes % 60)
    return f"{hours}時間{minutes}分"

def add_record_with_time(category: str, date_str: str, time_str: str, memo: str = "") -> None:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO records (category, time, memo) VALUES (?, ?, ?)",
        (category, f"{date_str} {time_str}", memo)
    )
    conn.commit()
    conn.close()