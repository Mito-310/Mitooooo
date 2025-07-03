import streamlit as st
import random
import math
import streamlit.components.v1 as components

# 初期化
if 'current_selection' not in st.session_state:
    st.session_state.current_selection = []
if 'target_words' not in st.session_state:
    st.session_state.target_words = []
if 'found_words' not in st.session_state:
    st.session_state.found_words = []

# ユーザーにレベルを選択させる
level = st.selectbox("レベルを選択してください", ["レベル 1 (6文字)", "レベル 2 (8文字)", "レベル 3 (12文字)"])

# 正解単語を入力
st.subheader("正解単語を設定")
target_word_input = st.text_input("正解単語を入力してください（カンマで複数指定可能）", 
                                  placeholder="例: CAT,DOG,BIRD")

if target_word_input:
    words = [word.strip().upper() for word in target_word_input.split(',') if word.strip()]
    st.session_state.target_words = words
    st.write(f"設定された正解単語: {', '.join(words)}")

if st.session_state.found_words:
    st.success(f"見つけた単語: {', '.join(st.session_state.found_words)}")

# リセットボタン
if st.button("ゲームをリセット"):
    st.session_state.found_words = []
    st.rerun()

# レベルに応じて文字数を設定
if level == "レベル 1 (6文字)":
    num_letters = 6
elif level == "レベル 2 (8文字)":
    num_letters = 8
else:
    num_letters = 12

# ランダムな文字を生成
all_letters = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
random.seed(0)
letters = random.sample(all_letters, num_letters)

# 円形に並べるボタンのHTMLを生成
button_html = ''.join([
    f'''
    <button class="circle-button" id="button_{i}"
            data-letter="{letter}"
            data-index="{i}"
            style="left: {150 + 120 * math.cos(2 * math.pi * i / num_letters - math.pi/2) - 30}px;
                   top:  {150 + 120 * math.sin(2 * math.pi * i / num_letters - math.pi/2) - 30}px;">
        {letter}
    </button>
    ''' for i, letter in enumerate(letters)
])

# HTML + CSS + JavaScript を組み立て
full_html = f"""
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
    <style>
    body {{
        margin: 0;
        font-family: Arial, sans-serif;
        user-select: none;
        -webkit-user-select: none;
        -moz-user-select: none;
        -ms-user-select: none;
        touch-action: none;
        -webkit-touch-callout: none;
        -webkit-tap-highlight-color: transparent;
    canvas {{
        position: absolute;
        top: 0;
        left: 0;
        z-index: -1;
        touch-action: none;
    }}
    .circle-container {{
        position: relative;
        width: 300px;
        height: 300px;
        margin: 60px auto 40px auto;
        border: 2px solid #ccc;
        border-radius: 50%;
        touch-action: none;
    }}
    .circle-button {{
        position: absolute;
        width: 60px;
        height: 60px;
        border-radius: 50%;
        background-color: white;
        color: black;
        font-size: 20px;
        font-weight: bold;
        border: 2px solid #4CAF50;
        cursor: pointer;
        display: flex;
        justify-content: center;
        align-items: center;
        transition: background-color 0.2s ease-in-out, border-color 0.2s ease-in-out;
        touch-action: none;
        -webkit-touch-callout: none;
        -webkit-tap-highlight-color: transparent;
    }}
    .circle-button.selected {{
        background-color: #FF5722;
        border-color: #FF5722;
        color: white;
    }}
    .circle-button:hover {{
        background-color: #f0f0f0;
    }}
    #selected-word {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        text-align: center;
        font-size: 28px;
        font-weight: bold;
        padding-top: 10px;
        user-select: none;
        letter-spacing: 4px;
        min-height: 40px;
        color: #FF5722;
        background-color: #fff;
        z-index: 999;
        border-bottom: 2px solid #FF5722;
        touch-action: none;
    }}
    canvas {{
        position: absolute;
        top: 0;
        left: 0;
        z-index: -1;
        touch-action: none;
    }}
    </style>
</head>
<body>
<div id="selected-word"></div>
<div id="target-words">正解単語: {', '.join(st.session_state.target_words) if st.session_state.target_words else '未設定'}</div>
<div id="found-words">見つけた単語: {', '.join(st.session_state.found_words) if st.session_state.found_words else 'なし'}</div>
<div id="success-message" class="success-message">正解！</div>

<div class="circle-container" id="circle-container">
    {button_html}
    <canvas id="lineCanvas" width="300" height="300"></canvas>
</div>

<script>
    let isInteracting = false;
    let selectedLetters = [];
    let selectedButtons = [];
    let points = [];
    let targetWords = {st.session_state.target_words};
    let foundWords = {st.session_state.found_words};

    const selectedWordDiv = document.getElementById('selected-word');
    const targetWordsDiv = document.getElementById('target-words');
    const foundWordsDiv = document.getElementById('found-words');
    const successMessageDiv = document.getElementById('success-message');
    const container = document.getElementById('circle-container');
    const canvas = document.getElementById('lineCanvas');
    const ctx = canvas.getContext('2d');

    function updateSelectedWord() {{
        selectedWordDiv.textContent = selectedLetters.join('');
    }}

    function checkCorrectWord() {{
        const currentWord = selectedLetters.join('');
        if (currentWord && targetWords.includes(currentWord) && !foundWords.includes(currentWord)) {{
            foundWords.push(currentWord);
            foundWordsDiv.textContent = '見つけた単語: ' + (foundWords.length ? foundWords.join(', ') : 'なし');
            showSuccessMessage();
            window.parent.postMessage({{type: 'correct-word', word: currentWord}}, '*');
            return true;
        }}
        return false;
    }}

    function showSuccessMessage() {{
        successMessageDiv.classList.add('show');
        setTimeout(() => {{
            successMessageDiv.classList.remove('show');
        }}, 2000);
    }}

    function getRelativeCenterPosition(elem, container) {{
        const elemRect = elem.getBoundingClientRect();
        const containerRect = container.getBoundingClientRect();
        const centerX = elemRect.left - containerRect.left + elem.offsetWidth / 2;
        const centerY = elemRect.top - containerRect.top + elem.offsetHeight / 2;
        return {{ x: centerX, y: centerY }};
    }}

    function resetSelection() {{
        selectedLetters = [];
        selectedButtons = [];
        points = [];
        document.querySelectorAll('.circle-button').forEach(button => {{
            button.classList.remove('selected');
        }});
        updateSelectedWord();
        drawLine();
    }}

    function selectButton(button) {{
        if (!selectedButtons.includes(button)) {{
            button.classList.add('selected');
            selectedLetters.push(button.dataset.letter);
            selectedButtons.push(button);
            points.push(getRelativeCenterPosition(button, container));
            drawLine();
            updateSelectedWord();
        }}
    }}

    function getButtonAtPosition(x, y) {{
        const buttons = document.querySelectorAll('.circle-button');
        for (let button of buttons) {{
            const rect = button.getBoundingClientRect();
            const containerRect = container.getBoundingClientRect();
            const relativeX = x - containerRect.left;
            const relativeY = y - containerRect.top;
            const buttonX = rect.left - containerRect.left;
            const buttonY = rect.top - containerRect.top;
            
            if (relativeX >= buttonX && relativeX <= buttonX + rect.width &&
                relativeY >= buttonY && relativeY <= buttonY + rect.height) {{
                return button;
            }}
        }}
        return null;
    }}

    // マウスイベント
    function handleMouseDown(event) {{
        isInteracting = true;
        const button = event.target.closest('.circle-button');
        if (button) {{
            selectButton(button);
        }}
        event.preventDefault();
    }}

    function handleMouseMove(event) {{
        if (!isInteracting) return;
        
        const button = getButtonAtPosition(event.clientX, event.clientY);
        if (button) {{
            selectButton(button);
        }}
        event.preventDefault();
    }}

    function handleMouseUp(event) {{
        if (isInteracting) {{
            isInteracting = false;
            const isCorrect = checkCorrectWord();
            setTimeout(() => {{
                resetSelection();
            }}, isCorrect ? 2000 : 500);
        }}
        event.preventDefault();
    }}

    // タッチイベント
    function handleTouchStart(event) {{
        isInteracting = true;
        const touch = event.touches[0];
        const button = getButtonAtPosition(touch.clientX, touch.clientY);
        if (button) {{
            selectButton(button);
        }}
        event.preventDefault();
    }}

    function handleTouchMove(event) {{
        if (!isInteracting) return;
        
        const touch = event.touches[0];
        const button = getButtonAtPosition(touch.clientX, touch.clientY);
        if (button) {{
            selectButton(button);
        }}
        event.preventDefault();
    }}

    function handleTouchEnd(event) {{
        if (isInteracting) {{
            isInteracting = false;
            const isCorrect = checkCorrectWord();
            setTimeout(() => {{
                resetSelection();
            }}, isCorrect ? 2000 : 500);
        }}
        event.preventDefault();
    }}

    function drawLine() {{
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        if(points.length === 0) return;

        ctx.beginPath();
        ctx.moveTo(points[0].x, points[0].y);
        points.forEach(point => {{
            ctx.lineTo(point.x, point.y);
        }});
        ctx.strokeStyle = '#FF5722';
        ctx.lineWidth = 3;
        ctx.lineCap = 'round';
        ctx.lineJoin = 'round';
        ctx.stroke();
    }}

    // イベントリスナーの設定
    container.addEventListener('mousedown', handleMouseDown);
    container.addEventListener('mousemove', handleMouseMove);
    container.addEventListener('mouseup', handleMouseUp);
    container.addEventListener('mouseleave', handleMouseUp);

    container.addEventListener('touchstart', handleTouchStart, {{passive: false}});
    container.addEventListener('touchmove', handleTouchMove, {{passive: false}});
    container.addEventListener('touchend', handleTouchEnd, {{passive: false}});
    container.addEventListener('touchcancel', handleTouchEnd, {{passive: false}});

    // 全体のイベントリスナー（タッチが範囲外に出た場合の処理）
    document.addEventListener('mouseup', function() {{
        if(isInteracting) {{
            isInteracting = false;
            const isCorrect = checkCorrectWord();
            setTimeout(() => {{
                resetSelection();
            }}, isCorrect ? 2000 : 500);
        }}
    }});

    document.addEventListener('touchend', function() {{
        if(isInteracting) {{
            isInteracting = false;
            const isCorrect = checkCorrectWord();
            setTimeout(() => {{
                resetSelection();
            }}, isCorrect ? 2000 : 500);
        }}
    }});
</script>
</body>
</html>
"""

# Streamlitの表示
st.title("Word Connect")
st.write("マウスまたはタッチ操作でボタンを順に選んでください。")

# components.html()で表示
components.html(full_html, height=500)