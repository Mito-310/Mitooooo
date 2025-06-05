import streamlit as st
import random

# 英検2級頻出単語リスト（例）
words = [
    'agree', 'allow', 'attach', 'avoid', 'book', 'cause', 'contact', 'contain',
    'continue', 'cost', 'cover', 'create', 'damage', 'develop', 'form', 'increase',
    'land', 'last', 'lead', 'leave', 'let', 'long', 'meet', 'offer', 'own', 'pay',
    'point', 'prevent', 'produce', 'protect', 'provide', 'recognize', 'recommend',
    'reduce', 'remove', 'run', 'ship', 'spread', 'treat'
]

# ゲームの状態を保存
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'target_word' not in st.session_state:
    st.session_state.target_word = random.choice(words)
    st.session_state.shuffled = list(st.session_state.target_word)
    random.shuffle(st.session_state.shuffled)
    st.session_state.answered = False  # 回答済みフラグ

st.title("🧩 英検2級 単語並び替えパズル")

st.markdown("バラバラの文字を並び替えて正しい英単語を当ててください！")

# 現在のスコア表示
st.subheader(f"🎯 スコア: {st.session_state.score}")

# シャッフルされた文字の表示
st.write("🔤 シャッフルされた文字:")
st.write(" ".join(st.session_state.shuffled))

# ユーザー入力
user_input = st.text_input("正しい単語を入力してください（小文字）:")

# 判定ボタン
if st.button("判定！") and not st.session_state.answered:
    if user_input == st.session_state.target_word:
        st.success("🎉 正解です！")
        st.session_state.score += 1
    else:
        st.error("❌ 不正解です。もう一度試してみてください。")
    st.session_state.answered = True

# 次の問題ボタン
if st.button("次の問題へ"):
    st.session_state.target_word = random.choice(words)
    st.session_state.shuffled = list(st.session_state.target_word)
    random.shuffle(st.session_state.shuffled)
    st.session_state.answered = False
    st.experimental_rerun()
