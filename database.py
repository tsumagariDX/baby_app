import streamlit as st
from datetime import datetime, timezone, timedelta
from supabase import create_client

JST = timezone(timedelta(hours=9))

def get_db():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

def add_record(category: str, memo: str = "") -> None:
    db = get_db()
    now = datetime.now(JST).strftime("%m/%d %H:%M")
    db.table("records").insert({
        "category": category,
        "time": now,
        "memo": memo
    }).execute()

def add_record_with_time(category: str, date_str: str, time_str: str, memo: str = "") -> None:
    db = get_db()
    db.table("records").insert({
        "category": category,
        "time": f"{date_str} {time_str}",
        "memo": memo
    }).execute()

def get_records_by_date(date_str: str) -> list:
    db = get_db()
    result = db.table("records").select("*").like("time", f"{date_str}%").order("id", desc=True).execute()
    return [(r["id"], r["category"], r["time"], r["memo"]) for r in result.data]

def delete_record(record_id: int) -> None:
    db = get_db()
    db.table("records").delete().eq("id", record_id).execute()

def get_count_by_date(category: str, date_str: str) -> int:
    db = get_db()
    result = db.table("records").select("*").eq("category", category).like("time", f"{date_str}%").execute()
    return len(result.data)

def get_sleep_time(date_str: str) -> str:
    db = get_db()
    result = db.table("records").select("*").in_("category", ["入眠", "起床"]).like("time", f"{date_str}%").order("id").execute()
    
    total_minutes = 0
    last_sleep = None

    for r in result.data:
        if r["category"] == "入眠":
            last_sleep = r["time"]
        elif r["category"] == "起床" and last_sleep is not None:
            sleep_time = datetime.strptime(last_sleep, "%m/%d %H:%M")
            wake_time = datetime.strptime(r["time"], "%m/%d %H:%M")
            diff = (wake_time - sleep_time).total_seconds() / 60
            total_minutes += diff
            last_sleep = None

    hours = int(total_minutes // 60)
    minutes = int(total_minutes % 60)
    return f"{hours}時間{minutes}分"