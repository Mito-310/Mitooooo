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

# 単語を四角（空欄）に変換する関数
def word_to_boxes(word, found=False):
    if found:
        return ' '.join(word)
    else:
        return ' '.join(['□'] * len(word))

# タイトル画面
if st.session_state.game_state == 'title':
    st.markdown("""
    <div style="text-align: center; padding: 50px;">
        <h1 style="font-size: 48px; color: #FF5722; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">
             Word Connect 
        </h1>
        <p style="font-size: 24px; color: #666; margin: 30px 0;">
            文字を繋げて単語を作ろう！
        </p>
        <p style="font-size: 18px; color: #999; margin: 20px 0;">
            マウスドラッグやスワイプで文字を繋げてください
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("START", use_container_width=True, type="primary"):
            st.session_state.game_state = 'stage_select'
            st.rerun()

# ステージ選択画面
elif st.session_state.game_state == 'stage_select':
    st.markdown("""
    <div style="text-align: center; padding: 30px;">
        <h2 style="color: #4CAF50;">ステージ選択</h2>
    </div>
    """, unsafe_allow_html=True)
    
    for stage_num, stage_info in STAGES.items():
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        color: white; padding: 20px; margin: 10px 0; 
                        border-radius: 10px; text-align: center;">
                <h3>{stage_info['name']}</h3>
                <p>文字数: {len(stage_info['letters'])}個</p>
                <p>単語数: {len(stage_info['words'])}個</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"選択", key=f"stage_{stage_num}", use_container_width=True):
                st.session_state.current_stage = stage_num
                st.session_state.target_words = STAGES[stage_num]['words']
                st.session_state.found_words = []
                st.session_state.game_state = 'game'
                st.rerun()
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("←タイトルに戻る", use_container_width=True):
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
        if st.button("⬅️ 戻る"):
            st.session_state.game_state = 'stage_select'
            st.rerun()
    with col2:
        st.markdown(f"<h3 style='text-align: center; color: #4CAF50;'>{current_stage_info['name']}</h3>", unsafe_allow_html=True)
    with col3:
        if st.button("🔄 リセット"):
            st.session_state.found_words = []
            st.rerun()
    
    # 進行状況
    progress = len(st.session_state.found_words) / len(st.session_state.target_words)
    st.progress(progress)
    st.write(f"進行状況: {len(st.session_state.found_words)} / {len(st.session_state.target_words)} 単語")
    
    # 目標単語の四角表示を生成
    target_boxes_html = []
    for word in st.session_state.target_words:
        is_found = word in st.session_state.found_words
        boxes = word_to_boxes(word, is_found)
        color = '#4CAF50' if is_found else '#999'
        target_boxes_html.append(f'<span style="color: {color}; font-weight: bold;">{boxes}</span>')
    
    target_display = ' | '.join(target_boxes_html)
    
    # 見つけた単語の表示
    found_display = ', '.join(st.session_state.found_words) if st.session_state.found_words else 'なし'
    
    # 円形に並べるボタンのHTMLを生成
    button_html = ''.join([
        f'''
        <div class="circle-button" id="button_{i}"
                data-letter="{letter}"
                data-index="{i}"
                style="left: {150 + 120 * math.cos(2 * math.pi * i / num_letters - math.pi/2) - 30}px;
                       top:  {150 + 120 * math.sin(2 * math.pi * i / num_letters - math.pi/2) - 30}px;">
            {letter}
        </div>
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
            overflow: hidden;
        }}
        .circle-container {{
            position: relative;
            width: 300px;
            height: 300px;
            margin: 100px auto 40px auto;
            border: 2px solid #ccc;
            border-radius: 50%;
            touch-action: none;
            background: linear-gradient(45deg, #f0f8ff, #e6f3ff);
        }}
        .circle-button {{
            position: absolute;
            width: 60px;
            height: 60px;
            border-radius: 50%;
            background: linear-gradient(145deg, #ffffff, #f0f0f0);
            color: #333;
            font-size: 20px;
            font-weight: bold;
            border: 2px solid #4CAF50;
            cursor: pointer;
            display: flex;
            justify-content: center;
            align-items: center;
            transition: all 0.3s ease;
            touch-action: none;
            -webkit-touch-callout: none;
            -webkit-tap-highlight-color: transparent;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }}
        .circle-button.selected {{
            background: linear-gradient(145deg, #FF5722, #E64A19);
            border-color: #FF5722;
            color: white;
            transform: scale(1.1);
            box-shadow: 0 6px 12px rgba(255,87,34,0.4);
        }}
        .circle-button:hover {{
            transform: scale(1.05);
            box-shadow: 0 6px 12px rgba(0,0,0,0.3);
        }}
        .circle-button.hover {{
            transform: scale(1.05);
            box-shadow: 0 6px 12px rgba(0,0,0,0.3);
        }}
        #selected-word {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            text-align: center;
            font-size: 32px;
            font-weight: bold;
            padding: 15px;
            user-select: none;
            letter-spacing: 6px;
            min-height: 50px;
            color: #FF5722;
            background: linear-gradient(135deg, #fff, #f8f8f8);
            z-index: 999;
            border-bottom: 3px solid #FF5722;
            touch-action: none;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        }}
        #target-words {{
            position: fixed;
            top: 70px;
            left: 0;
            width: 100%;
            text-align: center;
            font-size: 16px;
            font-weight: bold;
            padding: 10px;
            user-select: none;
            color: #666;
            background: linear-gradient(135deg, #e8f5e8, #f0f8f0);
            z-index: 998;
            border-bottom: 1px solid #ddd;
            touch-action: none;
            line-height: 1.5;
        }}
        #found-words {{
            position: fixed;
            top: 120px;
            left: 0;
            width: 100%;
            text-align: center;
            font-size: 14px;
            padding: 8px;
            user-select: none;
            color: #2196F3;
            background: linear-gradient(135deg, #e3f2fd, #f0f8ff);
            z-index: 997;
            border-bottom: 1px solid #ddd;
            touch-action: none;
            min-height: 25px;
        }}
        .success-message {{
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: linear-gradient(135deg, #4CAF50, #45a049);
            color: white;
            padding: 30px;
            border-radius: 15px;
            font-size: 28px;
            font-weight: bold;
            z-index: 1000;
            opacity: 0;
            transition: all 0.5s ease;
            box-shadow: 0 10px 30px rgba(76,175,80,0.3);
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        .success-message.show {{
            opacity: 1;
            transform: translate(-50%, -50%) scale(1.1);
        }}
        .complete-message {{
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: linear-gradient(135deg, #FF6B6B, #FF5722);
            color: white;
            padding: 40px;
            border-radius: 20px;
            font-size: 32px;
            font-weight: bold;
            z-index: 1001;
            opacity: 0;
            transition: all 0.5s ease;
            box-shadow: 0 15px 40px rgba(255,107,107,0.4);
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        .complete-message.show {{
            opacity: 1;
            transform: translate(-50%, -50%) scale(1.1);
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
    <div id="success-message" class="success-message">正解！ </div>
    <div id="complete-message" class="complete-message">ステージクリア！ </div>

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
                const color = isFound ? '#4CAF50' : '#999';
                return `<span style="color: ${{color}}; font-weight: bold;">${{boxes}}</span>`;
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
                
                // 全ての単語を見つけた場合
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
            }}, 2000);
        }}

        function showCompleteMessage() {{
            completeMessageDiv.classList.add('show');
            setTimeout(() => {{
                completeMessageDiv.classList.remove('show');
            }}, 3000);
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
                // 前のホバーボタンからhoverクラスを除去
                if (currentHoverButton && !selectedButtons.includes(currentHoverButton)) {{
                    currentHoverButton.classList.remove('hover');
                }}
                
                // 新しいホバーボタンにhoverクラスを追加
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
                }}, isCorrect ? 1500 : 300);
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
                }}, isCorrect ? 1500 : 300);
            }}
        }}

        function drawLine() {{
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            if (points.length < 2) return;

            // グラデーション効果のある線を描画
            ctx.beginPath();
            ctx.moveTo(points[0].x, points[0].y);
            
            for (let i = 1; i < points.length; i++) {{
                ctx.lineTo(points[i].x, points[i].y);
            }}
            
            // 線のスタイル設定
            ctx.strokeStyle = '#FF5722';
            ctx.lineWidth = 4;
            ctx.lineCap = 'round';
            ctx.lineJoin = 'round';
            ctx.shadowColor = 'rgba(255, 87, 34, 0.4)';
            ctx.shadowBlur = 6;
            ctx.stroke();

            // 点を描画
            points.forEach(point => {{
                ctx.beginPath();
                ctx.arc(point.x, point.y, 3, 0, 2 * Math.PI);
                ctx.fillStyle = '#FF5722';
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
        st.success("Stage Clear！おめでとうございます！")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("タイトルに戻る", use_container_width=True):
                st.session_state.game_state = 'title'
                st.rerun()
        with col2:
            if st.button("ステージ選択", use_container_width=True):
                st.session_state.game_state = 'stage_select'
                st.rerun()