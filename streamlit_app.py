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
    body {{
        margin: 0;
        font-family: Arial, sans-serif;
        user-select: none;
    }}
    .circle-container {{
        position: relative;
        width: 300px;
        height: 300px;
        margin: 60px auto 40px auto;
        border: 2px solid #ccc;
        border-radius: 50%;
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
        width: 100%;
        text-align: center;
        font-size: 28px;
        font-weight: bold;
        padding-top: 10px;
        user-select: none;
        letter-spacing: 4px;
        min-height: 40px;
        color: #FF5722;
    }}
    canvas {{
        position: absolute;
        top: 0;
        left: 0;
        z-index: -1;
    }}
    </style>
</head>
<body>
<div id="selected-word"></div>

<div class="circle-container" id="circle-container">
    {button_html}
    <canvas id="lineCanvas" width="300" height="300"></canvas>
</div>

<script>
    let isMouseDown = false;
    let selectedLetters = [];
    let points = [];

    const selectedWordDiv = document.getElementById('selected-word');
    const container = document.getElementById('circle-container');

    function updateSelectedWord() {{
        selectedWordDiv.textContent = selectedLetters.join('');
    }}

    function getRelativeCenterPosition(elem, container) {{
        const elemRect = elem.getBoundingClientRect();
        const containerRect = container.getBoundingClientRect();
        const centerX = elemRect.left - containerRect.left + elem.offsetWidth / 2;
        const centerY = elemRect.top - containerRect.top + elem.offsetHeight / 2;
        return {{ x: centerX, y: centerY }};
    }}

    document.querySelectorAll('.circle-button').forEach(button => {{
        button.addEventListener('mousedown', handlePointerDown);
        button.addEventListener('mouseenter', handlePointerMove);
        button.addEventListener('mouseup', handlePointerUp);
        
        button.addEventListener('touchstart', handlePointerDown);
        button.addEventListener('touchmove', handlePointerMove);
        button.addEventListener('touchend', handlePointerUp);
    }});

    function handlePointerDown(event) {{
        isMouseDown = true;
        let target = event.target;
        if (event.type.startsWith('touch')) {{
            target = event.touches[0].target;
        }}
        if (!target.classList.contains('selected')) {{
            target.classList.add('selected');
            selectedLetters.push(target.dataset.letter);
            points.push(getRelativeCenterPosition(target, container));
            drawLine();
            updateSelectedWord();
        }}
        event.preventDefault();
    }}

    function handlePointerMove(event) {{
        if (isMouseDown) {{
            let target = event.target;
            if (event.type.startsWith('touch')) {{
                target = event.touches[0].target;
            }}
            if (!target.classList.contains('selected')) {{
                target.classList.add('selected');
                selectedLetters.push(target.dataset.letter);
                points.push(getRelativeCenterPosition(target, container));
                drawLine();
                updateSelectedWord();
            }}
        }}
        event.preventDefault();
    }}

    function handlePointerUp(event) {{
        isMouseDown = false;
        const queryString = selectedLetters.join(',');
        window.parent.postMessage({{type: 'letters', data: queryString}}, '*');
        event.preventDefault();
    }}

    function drawLine() {{
        const canvas = document.getElementById('lineCanvas');
        const ctx = canvas.getContext('2d');
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        if(points.length === 0) return;

        ctx.beginPath();
        ctx.moveTo(points[0].x, points[0].y);
        points.forEach(point => {{
            ctx.lineTo(point.x, point.y);
        }});
        ctx.strokeStyle = '#FF5722';
        ctx.lineWidth = 3;
        ctx.stroke();
    }}

    document.addEventListener('mouseup', function() {{
        if(isMouseDown) {{
            isMouseDown = false;
            const queryString = selectedLetters.join(',');
            window.parent.postMessage({{type: 'letters', data: queryString}}, '*');
        }}
    }});
</script>
</body>
</html>
"""

st.title("Word Connect")
st.write("マウスまたはタッチ操作でボタンを順に選んでください。")

components.html(full_html, height=500)
