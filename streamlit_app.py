import streamlit as st
import random

# タイトル
st.title("じゃんけんゲーム ✊✌️🖐")

# ユーザーの手を選ぶ
user_choice = st.radio("あなたの手を選んでください：", ("グー", "チョキ", "パー"))

# 対戦ボタン
if st.button("じゃんけん！"):
    # コンピュータの手をランダムに選ぶ
    choices = ["グー", "チョキ", "パー"]
    computer_choice = random.choice(choices)

    # 勝敗判定
    if user_choice == computer_choice:
        result = "あいこです！"
    elif (user_choice == "グー" and computer_choice == "チョキ") or \
         (user_choice == "チョキ" and computer_choice == "パー") or \
         (user_choice == "パー" and computer_choice == "グー"):
        result = "あなたの勝ち！🎉"
    else:
        result = "あなたの負け...😢"

    # 結果表示
    st.subheader("結果")
    st.write(f"あなたの手：{user_choice}")
    st.write(f"コンピュータの手：{computer_choice}")
    st.success(result)
 