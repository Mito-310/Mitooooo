import streamlit as st
import random
import math
import streamlit.components.v1 as components

# 初期化
if 'game_state' not in st.session_state:
    st.session_state.game_state = 'title'  # 'title', 'stage_select', 'game'
if 'current_stage' not in st.session_state:
    st.session_state.current_stage = 1
if 'target_words' not in st.session_state:
    st.session_state.target_words = []
if 'found_words' not in st.session_state:
    st.session_state.found_words = []

# ステージ設定
STAGES = {
    1: {
        'name': 'ステージ 1',
        'letters': ['C', 'A', 'T', 'D', 'O', 'G'],
        'words': ['CAT', 'DOG', 'COD', 'TAG', 'GOD', 'COG']
    },
    2: {
        'name': 'ステージ 2',
        'letters': ['R', 'E', 'D', 'B', 'L', 'U', 'E', 'G'],
        'words': ['RED', 'BLUE', 'BED', 'LED', 'RUB', 'BUG', 'GEL', 'LEG']
    },
    3: {
        'name': 'ステージ 3',
        'letters': ['B', 'R', 'E', 'A', 'D', 'C', 'A', 'K', 'E', 'F', 'I', 'S'],
        'words': ['BREAD', 'CAKE', 'FISH', 'RICE', 'BEEF', 'DESK', 'FIRE', 'SAKE', 'FACE', 'DEAR']
    }
}

# タイトル画面
if st.session_state.game_state == 'title':
    st.title("Word Connect")
    st.write("文字を繋げて単語を作ろう")
    
    if st.button("START"):
        st.session_state.game_state = 'stage_select'
        st.rerun()

# ステージ選択画面
elif st.session_state.game_state == 'stage_select':
    st.header("ステージ選択")
    
    for stage_num, stage_info in STAGES.items():
        with st.container():
            st.subheader(stage_info['name'])
            st.write(f"文字数: {len(stage_info['letters'])}個")
            st.write(f"単語数: {len(stage_info['words'])}個")
            
            if st.button(f"選択", key=f"stage_{stage_num}"):
                st.session_state.current_stage = stage_num
                st.session_state.target_words = STAGES[stage_num]['words']
                st.session_state.found_words = []
                st.session_state.game_state = 'game'
                st.rerun()
    
    if st.button("← タイトルに戻る"):
        st.session_state.game_state = 'title'
        st.rerun()

# ゲーム画面
elif st.session_state.game_state == 'game':
    current_stage_info = STAGES[st.session_state.current_stage]
    letters = current_stage_info['letters']
    num_letters = len(letters)
    
    # ヘッダー
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("⬅戻る"):
            st.session_state.game_state = 'stage_select'
            st.rerun()
    with col2:
        st.header(current_stage_info['name'])
    with col3:
        if st.button("リセット"):
            st.session_state.found_words = []
            st.rerun()
    
    # 進行状況
    progress = len(st.session_state.found_words) / len(st.session_state.target_words)
    st.progress(progress)
    st.write(f"進行状況: {len(st.session_state.found_words)} / {len(st.session_state.target_words)} 単語")
    
    # 目標単語の表示
    sorted_words = sorted(st.session_state.target_words)
    target_boxes_html = []
    
    for word in sorted_words:
        is_found = word in st.session_state.found_words
        boxes_html = ""
        for letter in word:
            if is_found:
                boxes_html += f'<span style="display: inline-block; width: 20px; height: 20px; border: 1px solid #333; background: #4CAF50; color: white; text-align: center; line-height: 18px; margin: 1px; font-size: 12px;">{letter}</span>'
            else:
                boxes_html += f'<span style="display: inline-block; width: 20px; height: 20px; border: 1px solid #333; background: white; text-align: center; line-height: 18px; margin: 1px;"></span>'
        target_boxes_html.append(f'<div style="display: inline-block; margin: 5px;">{boxes_html}</div>')
    
    target_display = ' '.join(target_boxes_html)
    
    # 見つけた単語の表示
    found_display = ', '.join(st.session_state.found_words) if st.session_state.found_words else 'なし'
    
    # 円形に並べるボタンのHTMLを生成
    button_html = ''.join([
        f'''
        <div class="circle-button" id="button_{i}"
                data-letter="{letter}"
                data-index="{i}"
                style="left: {150 + 120 * math.cos(2 * math.pi * i / num_letters - math.pi/2) - 25}px;
                       top:  {150 + 120 * math.sin(2 * math.pi * i / num_letters - math.pi/2) - 25}px;">
            {letter}
        </div>
        ''' for i, letter in enumerate(letters)
    ])

    # シンプルなHTML + CSS + JavaScript
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
            overflow: hidden;
        }}
        .circle-container {{
            position: relative;
            width: 300px;
            height: 300px;
            margin: 150px auto 40px auto;
            border: 2px solid #ccc;
            border-radius: 50%;
            touch-action: none;
            background: #f9f9f9;
        }}
        .circle-button {{
            position: absolute;
            width: 50px;
            height: 50px;
            border-radius: 50%;
            background: white;
            color: #333;
            font-size: 18px;
            font-weight: bold;
            border: 2px solid #333;
            cursor: pointer;
            display: flex;
            justify-content: center;
            align-items: center;
            transition: all 0.2s ease;
            touch-action: none;
            -webkit-touch-callout: none;
            -webkit-tap-highlight-color: transparent;
        }}
        .circle-button.selected {{
            background: #333;
            color: white;
        }}
        .circle-button:hover {{
            background: #f0f0f0;
        }}
        .circle-button.hover {{
            background: #f0f0f0;
        }}
        #selected-word {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            text-align: center;
            font-size: 24px;
            font-weight: bold;
            padding: 10px;
            user-select: none;
            letter-spacing: 4px;
            min-height: 40px;
            color: #333;
            background: white;
            z-index: 999;
            border-bottom: 1px solid #ccc;
            touch-action: none;
        }}
        #target-words {{
            position: fixed;
            top: 60px;
            left: 0;
            width: 100%;
            text-align: center;
            font-size: 14px;
            padding: 10px;
            user-select: none;
            color: #666;
            background: #f9f9f9;
            z-index: 998;
            border-bottom: 1px solid #ccc;
            touch-action: none;
        }}
        #found-words {{
            position: fixed;
            top: 110px;
            left: 0;
            width: 100%;
            text-align: center;
            font-size: 12px;
            padding: 5px;
            user-select: none;
            color: #333;
            background: #f0f0f0;
            z-index: 997;
            border-bottom: 1px solid #ccc;
            touch-action: none;
            min-height: 20px;
        }}
        .success-message {{
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: #4CAF50;
            color: white;
            padding: 20px;
            border-radius: 5px;
            font-size: 18px;
            font-weight: bold;
            z-index: 1000;
            opacity: 0;
            transition: all 0.3s ease;
        }}
        .success-message.show {{
            opacity: 1;
        }}
        .complete-message {{
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: #2196F3;
            color: white;
            padding: 30px;
            border-radius: 5px;
            font-size: 24px;
            font-weight: bold;
            z-index: 1001;
            opacity: 0;
            transition: all 0.3s ease;
        }}
        .complete-message.show {{
            opacity: 1;
        }}
        canvas {{
            position: absolute;
            top: 0;
            left: 0;
            z-index: 1;
            touch-action: none;
            pointer-events: none;
        }}
        </style>
    </head>
    <body>
    <div id="selected-word"></div>
    <div id="target-words">{target_display}</div>
    <div id="found-words">見つけた単語: {found_display}</div>
    <div id="success-message" class="success-message">正解！</div>
    <div id="complete-message" class="complete-message">ステージクリア！</div>

    <div class="circle-container" id="circle-container">
        {button_html}
        <canvas id="lineCanvas" width="300" height="300"></canvas>
    </div>

    <script>
        let isDragging = false;
        let selectedLetters = [];
        let selectedButtons = [];
        let points = [];
        let targetWords = {st.session_state.target_words};
        let foundWords = {st.session_state.found_words};
        let currentHoverButton = null;

        const selectedWordDiv = document.getElementById('selected-word');
        const targetWordsDiv = document.getElementById('target-words');
        const foundWordsDiv = document.getElementById('found-words');
        const successMessageDiv = document.getElementById('success-message');
        const completeMessageDiv = document.getElementById('complete-message');
        const container = document.getElementById('circle-container');
        const canvas = document.getElementById('lineCanvas');
        const ctx = canvas.getContext('2d');

        function updateSelectedWord() {{
            selectedWordDiv.textContent = selectedLetters.join('');
        }}

        function updateTargetDisplay() {{
            const targetBoxes = targetWords.map(word => {{
                const isFound = foundWords.includes(word);
                const boxes = isFound ? word.split('').join(' ') : '□'.repeat(word.length).split('').join(' ');
                const color = isFound ? '#4CAF50' : '#666';
                return `<span style="color: ${{color}};">${{boxes}}</span>`;
            }});
            targetWordsDiv.innerHTML = targetBoxes.join(' | ');
        }}

        function checkCorrectWord() {{
            const currentWord = selectedLetters.join('');
            if (currentWord && targetWords.includes(currentWord) && !foundWords.includes(currentWord)) {{
                foundWords.push(currentWord);
                foundWordsDiv.textContent = '見つけた単語: ' + foundWords.join(', ');
                updateTargetDisplay();
                showSuccessMessage();
                
                if (foundWords.length === targetWords.length) {{
                    setTimeout(() => {{
                        showCompleteMessage();
                    }}, 1000);
                }}
                
                return true;
            }}
            return false;
        }}

        function showSuccessMessage() {{
            successMessageDiv.classList.add('show');
            setTimeout(() => {{
                successMessageDiv.classList.remove('show');
            }}, 1500);
        }}

        function showCompleteMessage() {{
            completeMessageDiv.classList.add('show');
            setTimeout(() => {{
                completeMessageDiv.classList.remove('show');
            }}, 2500);
        }}

        function getButtonCenterPosition(button) {{
            const rect = button.getBoundingClientRect();
            const containerRect = container.getBoundingClientRect();
            const centerX = rect.left - containerRect.left + rect.width / 2;
            const centerY = rect.top - containerRect.top + rect.height / 2;
            return {{ x: centerX, y: centerY }};
        }}

        function resetSelection() {{
            selectedLetters = [];
            selectedButtons = [];
            points = [];
            document.querySelectorAll('.circle-button').forEach(button => {{
                button.classList.remove('selected');
                button.classList.remove('hover');
            }});
            currentHoverButton = null;
            updateSelectedWord();
            drawLine();
        }}

        function selectButton(button) {{
            if (!selectedButtons.includes(button)) {{
                button.classList.add('selected');
                selectedLetters.push(button.dataset.letter);
                selectedButtons.push(button);
                points.push(getButtonCenterPosition(button));
                updateSelectedWord();
                drawLine();
            }}
        }}

        function getButtonAtPosition(x, y) {{
            const buttons = document.querySelectorAll('.circle-button');
            for (let button of buttons) {{
                const rect = button.getBoundingClientRect();
                if (x >= rect.left && x <= rect.right && y >= rect.top && y <= rect.bottom) {{
                    return button;
                }}
            }}
            return null;
        }}

        function handleHover(button) {{
            if (button !== currentHoverButton) {{
                if (currentHoverButton && !selectedButtons.includes(currentHoverButton)) {{
                    currentHoverButton.classList.remove('hover');
                }}
                
                if (button && !selectedButtons.includes(button)) {{
                    button.classList.add('hover');
                }}
                
                currentHoverButton = button;
            }}
        }}

        // マウスイベント
        function handleMouseDown(event) {{
            event.preventDefault();
            isDragging = true;
            const button = event.target.closest('.circle-button');
            if (button) {{
                selectButton(button);
                handleHover(button);
            }}
        }}

        function handleMouseMove(event) {{
            event.preventDefault();
            const button = getButtonAtPosition(event.clientX, event.clientY);
            
            if (isDragging && button) {{
                selectButton(button);
            }}
            
            handleHover(button);
        }}

        function handleMouseUp(event) {{
            event.preventDefault();
            if (isDragging) {{
                isDragging = false;
                const isCorrect = checkCorrectWord();
                setTimeout(() => {{
                    resetSelection();
                }}, isCorrect ? 1000 : 200);
            }}
        }}

        // タッチイベント
        function handleTouchStart(event) {{
            event.preventDefault();
            isDragging = true;
            const touch = event.touches[0];
            const button = getButtonAtPosition(touch.clientX, touch.clientY);
            if (button) {{
                selectButton(button);
                handleHover(button);
            }}
        }}

        function handleTouchMove(event) {{
            event.preventDefault();
            if (!isDragging) return;
            
            const touch = event.touches[0];
            const button = getButtonAtPosition(touch.clientX, touch.clientY);
            
            if (button) {{
                selectButton(button);
                handleHover(button);
            }}
        }}

        function handleTouchEnd(event) {{
            event.preventDefault();
            if (isDragging) {{
                isDragging = false;
                const isCorrect = checkCorrectWord();
                setTimeout(() => {{
                    resetSelection();
                }}, isCorrect ? 1000 : 200);
            }}
        }}

        function drawLine() {{
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            if (points.length < 2) return;

            ctx.beginPath();
            ctx.moveTo(points[0].x, points[0].y);
            
            for (let i = 1; i < points.length; i++) {{
                ctx.lineTo(points[i].x, points[i].y);
            }}
            
            ctx.strokeStyle = '#333';
            ctx.lineWidth = 2;
            ctx.stroke();

            points.forEach(point => {{
                ctx.beginPath();
                ctx.arc(point.x, point.y, 2, 0, 2 * Math.PI);
                ctx.fillStyle = '#333';
                ctx.fill();
            }});
        }}

        // イベントリスナーの設定
        container.addEventListener('mousedown', handleMouseDown);
        document.addEventListener('mousemove', handleMouseMove);
        document.addEventListener('mouseup', handleMouseUp);

        container.addEventListener('touchstart', handleTouchStart, {{passive: false}});
        container.addEventListener('touchmove', handleTouchMove, {{passive: false}});
        container.addEventListener('touchend', handleTouchEnd, {{passive: false}});

        // 初期化
        updateSelectedWord();
        updateTargetDisplay();
    </script>
    </body>
    </html>
    """

    # Streamlitの表示
    components.html(full_html, height=600)
    
    # ステージクリア判定
    if len(st.session_state.found_words) == len(st.session_state.target_words):
        st.balloons()
        st.success("Stage Clear")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("タイトルに戻る", use_container_width=True):
                st.session_state.game_state = 'title'
                st.rerun()
        with col2:
            if st.button("ステージ選択", use_container_width=True):
                st.session_state.game_state = 'stage_select'
                st.rerun()