import streamlit as st
import random
import math

# 初期化
if 'current_selection' not in st.session_state:
    st.session_state.current_selection = []

# 固定の12文字（テスト用にランダムに選択）
all_letters = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
random.seed(0)
letters = random.sample(all_letters, 12)

# タイトル
st.title("🕒 時計型ボタン配置（Word Connect）")
st.write("マウスを押しながらドラッグするとボタンを順番に押せます。")

# CSS と 円形配置コンテナ
st.markdown("""
    <style>
    .circle-container {
        position: relative;
        width: 300px;
        height: 300px;
        margin: 40px auto;
        border: 2px solid #ccc;
        border-radius: 50%;
    }
    .circle-button {
        position: absolute;
        width: 60px;
        height: 60px;
        border-radius: 50%;
        background-color: #4CAF50;
        color: white;
        font-size: 20px;
        font-weight: bold;
        border: none;
        cursor: pointer;
        display: flex;
        justify-content: center;
        align-items: center;
        transition: background-color 0.2s ease-in-out;
    }
    .circle-button:hover {
        background-color: #388E3C;
    }
    </style>
""", unsafe_allow_html=True)

# 円形配置ボタンのHTMLを生成
button_html = ''.join([
    f'''
    <button class="circle-button" id="button_{i}" 
            data-letter="{letter}" 
            style="
            left: {150 + 120 * math.cos(2 * math.pi * i / 12 - math.pi/2) - 30}px;
            top: {150 + 120 * math.sin(2 * math.pi * i / 12 - math.pi/2) - 30}px;">
            {letter}
    </button>
    ''' for i, letter in enumerate(letters)
])

# HTML + JavaScript をマークダウンで描画
st.markdown("""
<div class="circle-container" id="circle-container">
""" + button_html + """
</div>

<script>
document.addEventListener('DOMContentLoaded', function () {
    let isMouseDown = false;
    let selectedLetters = [];

    document.querySelectorAll('.circle-button').forEach(button => {
        button.addEventListener('mousedown', function(event) {
            isMouseDown = true;
            event.target.style.backgroundColor = '#388E3C';
            selectedLetters.push(event.target.dataset.letter);
        });

        button.addEventListener('mouseenter', function(event) {
            if (isMouseDown) {
                event.target.style.backgroundColor = '#388E3C';
                if (!selectedLetters.includes(event.target.dataset.letter)) {
                    selectedLetters.push(event.target.dataset.letter);
                }
            }
        });

        button.addEventListener('mouseup', function() {
            isMouseDown = false;
            const queryString = selectedLetters.join(',');
            window.history.pushState({}, '', '?letters=' + queryString); // ページ遷移せずにURLを更新
        });
    });
});
</script>
""", unsafe_allow_html=True)

# 文字選択をキャッチ
letters_clicked = st.query_params.get("letters", [])
if letters_clicked:
    st.session_state.current_selection = letters_clicked[0].split(',')

# 現在の選択
current_word = ''.join(st.session_state.current_selection)
st.write(f"### ✍️ 選択中の文字: **{current_word}**")

# アクションボタン
col1, col2 = st.columns(2)
with col1:
    if st.button("提出"):
        st.success(f"仮：『{current_word}』を提出しました（ここに単語判定処理を追加できます）")
        st.session_state.current_selection = []
with col2:
    if st.button("リセット"):
        st.session_state.current_selection = []
