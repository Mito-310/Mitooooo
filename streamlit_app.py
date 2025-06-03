import streamlit as st
import pandas as pd
import sqlite3

# SQLite DBに接続
conn = sqlite3.connect('essay_feedback.db')
cursor = conn.cursor()

# テーブルの作成
def create_tables():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS essays (
            id INTEGER PRIMARY KEY,
            user_name TEXT,
            essay_text TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY,
            essay_id INTEGER,
            user_name TEXT,
            feedback_text TEXT,
            rating INTEGER,
            FOREIGN KEY(essay_id) REFERENCES essays(id)
        )
    ''')
    conn.commit()

create_tables()

# 作文をデータベースに保存
def save_essay(user_name, essay_text):
    cursor.execute('''
        INSERT INTO essays (user_name, essay_text) VALUES (?, ?)
    ''', (user_name, essay_text))
    conn.commit()

# 添削をデータベースに保存
def save_feedback(essay_id, user_name, feedback_text, rating):
    cursor.execute('''
        INSERT INTO feedback (essay_id, user_name, feedback_text, rating) VALUES (?, ?, ?, ?)
    ''', (essay_id, user_name, feedback_text, rating))
    conn.commit()

# 作文を全て取得
def get_all_essays():
    cursor.execute('SELECT * FROM essays')
    return cursor.fetchall()

# 添削を特定の作文に関連づけて取得
def get_feedback_for_essay(essay_id):
    cursor.execute('SELECT * FROM feedback WHERE essay_id = ?', (essay_id,))
    return cursor.fetchall()

# Streamlit UI
def main():
    st.title('他人の作文、あなたならどう添削する？')
    
    # 作文投稿
    st.header('あなたの作文を投稿しよう')
    user_name = st.text_input('ユーザー名')
    essay_text = st.text_area('あなたの作文を入力してください:')
    
    if st.button('投稿する'):
        if user_name and essay_text:
            save_essay(user_name, essay_text)
            st.success('作文が投稿されました！')
        else:
            st.warning('ユーザー名と作文の内容を入力してください。')

    # 投稿された作文を表示
    st.header('他のユーザーの作文を添削しよう！')
    essays = get_all_essays()

    for essay in essays:
        essay_id, user_name, essay_text = essay
        st.subheader(f"作文（投稿者: {user_name}）")
        st.write(essay_text)
        
        # 添削入力フォーム
        feedback_text = st.text_area(f"この作文に対する添削を入力してください:", key=f'feedback_{essay_id}')
        rating = st.radio(f"この作文に対する評価を選んでください:", options=[1, 2, 3, 4, 5], key=f'rating_{essay_id}')
        
        if st.button(f"添削を投稿（作文ID: {essay_id})", key=f'button_{essay_id}'):
            if feedback_text:
                save_feedback(essay_id, user_name, feedback_text, rating)
                st.success('添削が投稿されました！')
            else:
                st.warning('添削内容を入力してください。')
        
        # 添削結果の表示
        feedbacks = get_feedback_for_essay(essay_id)
        if feedbacks:
            st.write('【添削内容】')
            for feedback in feedbacks:
                _, _, feedback_user, feedback_text, rating = feedback
                st.write(f"添削者: {feedback_user} 評価: {rating}")
                st.write(f"添削内容: {feedback_text}")
        else:
            st.write("まだ添削はありません。")

if __name__ == "__main__":
    main()
