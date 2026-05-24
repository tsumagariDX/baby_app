import streamlit as st
from datetime import datetime
from database import init_db, add_record, get_record, delete_record, get_count_by_date, get_records_by_date, get_sleep_time, add_record_with_time

# データベース初期化
init_db()

st.title("育児記録アプリ")

# ボタン
cols = st.columns(4)
labels = ["起床", "入眠", "授乳", "おむつ替え"]

if st.session_state.get("clear_quick_memo"):
    st.session_state.quick_memo = ""
    st.session_state.clear_quick_memo = False

memo_input = st.text_input("メモ（任意）", key="quick_memo")

for col, label in zip(cols, labels):
    with col:
        if st.button(label):
            add_record(label, memo_input)
            st.session_state.clear_quick_memo = True
            st.rerun()

st.subheader("手動で記録を追加")
col_a, col_b, col_c = st.columns([2, 2, 2])

with col_a:
    manual_category = st.selectbox("種類", ["起床", "入眠", "授乳", "おむつ替え"])
with col_b:
    manual_date = st.date_input("日付", key="manual_date")
with col_c:
    manual_time = st.time_input("時間")

if st.session_state.get("clear_manual_memo"):
    st.session_state.manual_memo = ""
    st.session_state.clear_manual_memo = False

manual_memo = st.text_input("メモ（任意）", key="manual_memo")

if st.button("追加"):
    date_str = manual_date.strftime("%m/%d")
    time_str = manual_time.strftime("%H:%M")
    add_record_with_time(manual_category, date_str, time_str, manual_memo)
    st.session_state.clear_manual_memo = True
    st.rerun()

# 記録表示
st.subheader("記録一覧")
selected_date = st.date_input("日付を選択")
date_str = selected_date.strftime("%m/%d")

cols2 = st.columns(3)

with cols2[0]:
    st.metric("睡眠時間", get_sleep_time(date_str))
with cols2[1]:
    st.metric("授乳", f"{get_count_by_date('授乳', date_str)}回")
with cols2[2]:
    st.metric("おむつ替え", f"{get_count_by_date('おむつ替え', date_str)}回")


records = get_records_by_date(date_str)

if records:
    for record in records:
        record_id, category, time, memo = record
        col1, col2 = st.columns([4, 1])
        with col1:
            if memo:
                st.write(f"{category} {time} 📝{memo}")
            else:
                st.write(f"{category} {time}")
        with col2:
            if st.button("削除", key=record_id):
                delete_record(record_id)
                st.rerun()
else:
    st.write("この日の記録はありません")