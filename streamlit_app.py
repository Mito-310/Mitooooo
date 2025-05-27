import streamlit as st
import random
import string
import nltk
from nltk.corpus import words

# 初回のみダウンロード
nltk.download('words')

# 英単語リスト
english_words = set(words.words())

# アプリのタイトル
st.title("アルファベット単語作成ゲーム")

# アルファベットの生成（初期化）
if 'letters' not in st.session_state:
    st.session_state.letters = random.sample(string.ascii_lowercase, 7)
    st.session_state.found_words = []

# 表示
st.subheader("使える文字:")
st.write(' '.join(st.session_state.letters).upper())

# 入力フォーム
user_input = st.text_input("文字を使って英単語を入力してください:")

# 単語をチェック
if user_input:
    word = user_input.lower()
    if all(word.count(c) <= st.session_state.letters.count(c) for c in word) and word in english_words:
        if word not in st.session_state.found_words:
            st.success(f"正解！: {word}")
            st.session_state.found_words.append(word)
        else:
            st.warning("その単語はすでに見つけています。")
    else:
        st.error("不正な単語です。もう一度試してください。")

# スコア表示
st.subheader("これまでに見つけた単語:")
st.write(st.session_state.found_words)

st.subheader("スコア:")
score = sum(len(word) for word in st.session_state.found_words)
st.write(f"{score} 点")

# リセットボタン
if st.button("ゲームをリセット"):
    st.session_state.letters = random.sample(string.ascii_lowercase, 7)
    st.session_state.found_words = []
