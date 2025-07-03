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
        'name': 'ステージ 1: 動物',
        'letters': ['C', 'A', 'T', 'D', 'O', 'G'],
        'words': ['CAT', 'DOG', 'COD', 'TAG', 'GOD', 'COG']
    },
    2: {
        'name': 'ステージ 2: 色',
        'letters': ['R', 'E', 'D', 'B', 'L', 'U', 'E', 'G'],
        'words': ['RED', 'BLUE', 'BED', 'LED', 'RUB', 'BUG', 'GEL', 'LEG']
    },
    3: {
        'name': 'ステージ 3: 食べ物',
        'letters': ['B', 'R', 'E', 'A', 'D', 'C', 'A', 'K', 'E', 'F', 'I', 'S'],
        'words': ['BREAD', 'CAKE', 'FISH', 'RICE', 'BEEF', 'DESK', 'FIRE', 'SAKE', 'FACE', 'DEAR']
    }
}

# タイトル画面
if st.session_state.game_state == 'title':
    st.markdown("""
    <div style="text-align: center; padding: 50px;">
        <h1 style="font-size: 48px; color: #FF5722; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">
            🎯 Word Connect 🎯
        </h1>
        <p style="font-size: 24px; color: #666; margin: 30px 0;">
            文字を繋げて単語を作ろう！
        </p>
        <p style="font-size: 18px; color: #999; margin: 20px 0;">
            指でスワイプして文字を繋げてください
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🎮 ゲーム開始", use_container_width=True, type="primary"):
            st.session_state.game_state = 'stage_select'
            st.rerun()

# ステージ選択画面
elif st.session_state.game_state == 'stage_select':
    st.markdown("""
    <div style="text-align: center; padding: 30px;">
        <h2 style="color: #4CAF50;">ステージを選択してください</h2>
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
            
            if st.button(f"ステージ {stage_num} を選択", key=f"stage_{stage_num}", use_container_width=True):
                st.session_state.current_stage = stage_num
                st.session_state.target_words = STAGES[stage_num]['words']
                st.session_state.found_words = []
                st.session_state.game_state = 'game'
                st.rerun()
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🏠 タイトルに戻る", use_container_width=True):
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
            color: #4CAF50;
            background: linear-gradient(135deg, #e8f5e8, #f0f8f0);
            z-index: 998;
            border-bottom: 1px solid #ddd;
            touch-action: none;
        }}
        #found-words {{
            position: fixed;
            top: 110px;
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
            z-index: -1;
            touch-action: none;
        }}
        </style>
    </head>
    <body>
    <div id="selected-word"></div>
    <div id="target-words">目標: {', '.join(st.session_state.target_words)}</div>
    <div id="found-words">見つけた単語: {', '.join(st.session_state.found_words) if st.session_state.found_words else 'なし'}</div>
    <div id="success-message" class="success-message">正解！ 🎉</div>
    <div id="complete-message" class="complete-message">ステージクリア！ 🏆</div>

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
        const completeMessageDiv = document.getElementById('complete-message');
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
                foundWordsDiv.textContent = '見つけた単語: ' + foundWords.join(', ');
                showSuccessMessage();
                
                // 全ての単語を見つけた場合
                if (foundWords.length === targetWords.length) {{
                    setTimeout(() => {{
                        showCompleteMessage();
                    }}, 1000);
                }}
                
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

        function showCompleteMessage() {{
            completeMessageDiv.classList.add('show');
            setTimeout(() => {{
                completeMessageDiv.classList.remove('show');
                window.parent.postMessage({{type: 'stage-complete'}}, '*');
            }}, 3000);
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

            // グラデーション効果のある線
            const gradient = ctx.createLinearGradient(0, 0, canvas.width, canvas.height);
            gradient.addColorStop(0, '#FF5722');
            gradient.addColorStop(1, '#FF8A65');

            ctx.beginPath();
            ctx.moveTo(points[0].x, points[0].y);
            points.forEach(point => {{
                ctx.lineTo(point.x, point.y);
            }});
            ctx.strokeStyle = gradient;
            ctx.lineWidth = 4;
            ctx.lineCap = 'round';
            ctx.lineJoin = 'round';
            ctx.shadowColor = 'rgba(255, 87, 34, 0.3)';
            ctx.shadowBlur = 8;
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

        // 全体のイベントリスナー
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
    components.html(full_html, height=600)
    
    # ステージクリア判定
    if len(st.session_state.found_words) == len(st.session_state.target_words):
        st.balloons()
        st.success("🎉 ステージクリア！おめでとうございます！")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🏠 タイトルに戻る", use_container_width=True):
                st.session_state.game_state = 'title'
                st.rerun()
        with col2:
            if st.button("📝 ステージ選択", use_container_width=True):
                st.session_state.game_state = 'stage_select'
                st.rerun()