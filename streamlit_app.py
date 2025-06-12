import streamlit as st
import random
import math
import streamlit.components.v1 as components

# 初期化
if 'current_selection' not in st.session_state:
    st.session_state.current_selection = []

# ランダムな12文字
all_letters = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
random.seed(0)
letters = random.sample(all_letters, 12)

# 円形に並べるボタンのHTMLを生成
button_html = ''.join([
    f'''
    <button class="circle-button" id="button_{i}"
            data-letter="{letter}"
            style="left: {150 + 120 * math.cos(2 * math.pi * i / 12 - math.pi/2) - 30}px;
                   top:  {150 + 120 * math.sin(2 * math.pi * i / 12 - math.pi/2) - 30}px;">
        {letter}
    </button>
    ''' for i, letter in enumerate(letters)
])

# HTML + CSS + JavaScript を組み立て
full_html = f"""
<html>
<head>
    <style>
    .circle-container {{
        position: relative;
        width: 300px;
        height: 300px;
        margin: 40px auto;
        border: 2px solid #ccc;
        border-radius: 50%;
    }}
    .circle-button {{
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
    }}
    .circle-button:hover {{
        background-color: #388E3C;
    }}
    </style>
</head>
<body>
<div class="circle-container" id="circle-container">
    {button_html}
</div>

<script>
    let isMouseDown = false;
    let selectedLetters = [];

    document.querySelectorAll('.circle-button').forEach(button => {{
        button.addEventListener('mousedown', function(event) {{
            isMouseDown = true;
            event.target.style.backgroundColor = '#388E3C';
            selectedLetters.push(event.target.dataset.letter);
        }});

        button.addEventListener('mouseenter', function(event) {{
            if (isMouseDown) {{
                event.target.style.backgroundColor = '#388E3C';
                if (!selectedLetters.includes(event.target.dataset.letter)) {{
                    selectedLetters.push(event.target.dataset.letter);
                }}
            }}
        }});

        button.addEventListener('mouseup', function() {{
            isMouseDown = false;
            const queryString = selectedLetters.join(',');
            window.parent.postMessage({{type: 'letters', data: queryString}}, '*');
        }});
    }});
</script>
</body>
</html>
"""

# タイトルと説明
st.title("🕒 時計型ボタン配置（Word Connect）")
st.write("マウスを押しながらドラッグするとボタンが順に選ばれます。")

# HTML を iframe で描画
components.html(full_html, height=400)

# クエリパラメータは使わず、postMessage 経由で JS と連携する場合も検討できます（次の段階で）
