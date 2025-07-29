import streamlit as st
import pandas as pd
import random
import math
import streamlit.components.v1 as components

# ページ設定
st.set_page_config(
    page_title="Word Connect Game",
    page_icon="🎮",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# カスタムCSS
st.markdown("""
<style>
    /* 全体のスタイル */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    /* メインコンテンツエリア */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* ヘッダーのスタイル */
    h1, h2, h3 {
        color: white !important;
        text-align: center;
    }
    
    /* プログレスバーのスタイル */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #4CAF50, #45a049);
    }
    
    /* テキストのスタイル */
    .stMarkdown, p, div {
        color: white !important;
    }
    
    /* ボタンのスタイル */
    .stButton > button {
        background: #000000 !important;
        color: white !important;
        border: 2px solid #333 !important;
        border-radius: 25px !important;
        font-weight: bold !important;
        font-size: 16px !important;
        padding: 0.5rem 2rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2) !important;
    }
    
    .stButton > button:hover {
        background: #333333 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(0,0,0,0.3) !important;
    }
    
    .stButton > button:active {
        transform: translateY(0px) !important;
    }
    
    /* 特別なボタンスタイル */
    .start-button {
        background: linear-gradient(45deg, #000000, #333333) !important;
        font-size: 20px !important;
        padding: 1rem 3rem !important;
        margin: 2rem 0 !important;
    }
    
    /* カードスタイル */
    .game-card {
        background: rgba(255,255,255,0.1);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        border: 1px solid rgba(255,255,255,0.2);
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    
    /* タイトルスタイル */
    .game-title {
        font-size: 4rem !important;
        font-weight: 900 !important;
        background: linear-gradient(45deg, #ffffff, #f0f0f0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin: 2rem 0 !important;
        text-shadow: 0 4px 8px rgba(0,0,0,0.3);
        letter-spacing: 2px;
    }
    
    .game-subtitle {
        font-size: 1.5rem !important;
        color: rgba(255,255,255,0.9) !important;
        text-align: center;
        margin-bottom: 3rem !important;
        font-weight: 300;
    }
    
    /* ルールカード */
    .rules-card {
        background: rgba(255,255,255,0.15);
        backdrop-filter: blur(15px);
        border-radius: 15px;
        padding: 2rem;
        margin: 2rem auto;
        max-width: 600px;
        border: 1px solid rgba(255,255,255,0.2);
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    
    .rules-card h3 {
        color: #ffffff !important;
        margin-bottom: 1rem !important;
        font-size: 1.5rem !important;
    }
    
    .rules-card p {
        color: rgba(255,255,255,0.9) !important;
        line-height: 1.6;
        margin-bottom: 0.8rem !important;
    }
    
    /* ステージ選択カード */
    .stage-cards {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin: 2rem 0;
    }
    
    .stage-card {
        background: rgba(255,255,255,0.1);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.2);
        transition: all 0.3s ease;
    }
    
    .stage-card:hover {
        transform: translateY(-5px);
        background: rgba(255,255,255,0.15);
        box-shadow: 0 10px 25px rgba(0,0,0,0.2);
    }
    
    /* ゲーム画面のスタイル */
    .game-header {
        background: rgba(255,255,255,0.1);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 1rem;
        margin-bottom: 2rem;
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    /* プログレス表示 */
    .progress-text {
        text-align: center;
        font-size: 1.2rem !important;
        color: white !important;
        margin: 1rem 0 !important;
        font-weight: 500;
    }
    
    /* 見つけた単語の表示 */
    .found-words-display {
        background: rgba(76, 175, 80, 0.2);
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        border: 1px solid rgba(76, 175, 80, 0.3);
    }
    
    /* エラー・警告メッセージのスタイル */
    .stAlert {
        background: rgba(255,255,255,0.1) !important;
        border-radius: 10px !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
    }
    
    /* サイドバーを非表示 */
    .css-1d391kg {
        display: none;
    }
</style>
""", unsafe_allow_html=True)

# 問題データ（デフォルト）
DEFAULT_STAGES = {
    1: {
        'name': 'ステージ 1',
        'problem_text': 'CATDOG',
        'letters': ['C', 'A', 'T', 'D', 'O', 'G'],
        'words': ['CAT', 'DOG', 'COD', 'TAG', 'GOD', 'COG']
    },
    2: {
        'name': 'ステージ 2',
        'problem_text': 'REDBLUE',
        'letters': ['R', 'E', 'D', 'B', 'L', 'U'],
        'words': ['RED', 'BLUE', 'BED', 'LED', 'RUB', 'BUG']
    },
    3: {
        'name': 'ステージ 3',
        'problem_text': 'BREADCAKE',
        'letters': ['B', 'R', 'E', 'A', 'D', 'C', 'K'],
        'words': ['BREAD', 'CAKE', 'DEAR', 'CARE', 'BEAR']
    },
    4: {
        'name': 'ステージ 4',
        'problem_text': 'SUNMOON',
        'letters': ['S', 'U', 'N', 'M', 'O'],
        'words': ['SUN', 'MOON', 'SON', 'NUN', 'MUN']
    },
    5: {
        'name': 'ステージ 5',
        'problem_text': 'FIREWATER',
        'letters': ['F', 'I', 'R', 'E', 'W', 'A', 'T'],
        'words': ['FIRE', 'WATER', 'WIFE', 'TIRE', 'WIRE', 'TEAR']
    }
}

# 初期化
if 'game_state' not in st.session_state:
    st.session_state.game_state = 'title'
if 'current_stage' not in st.session_state:
    st.session_state.current_stage = 1
if 'target_words' not in st.session_state:
    st.session_state.target_words = []
if 'found_words' not in st.session_state:
    st.session_state.found_words = []

STAGES = DEFAULT_STAGES

# タイトル画面
if st.session_state.game_state == 'title':
    # メインタイトル
    st.markdown('<h1 class="game-title">WORD CONNECT</h1>', unsafe_allow_html=True)
    st.markdown('<p class="game-subtitle">文字を繋げて単語を作ろう</p>', unsafe_allow_html=True)
    
    # ゲームルール
    st.markdown("""
    <div class="rules-card">
        <h3>🎮 ゲームルール</h3>
        <p>• 円形に配置された文字をドラッグして繋げて単語を作ります</p>
        <p>• すべての目標単語を見つけるとステージクリア！</p>
        <p>• 同じ文字を重複して使うことはできません</p>
        <p>• マウスまたはタッチで文字を選択してください</p>
    </div>
    """, unsafe_allow_html=True)
    
    # STARTボタン
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 ゲームスタート", key="start_button", use_container_width=True):
            st.session_state.current_stage = 1
            st.session_state.target_words = STAGES[1]['words']
            st.session_state.found_words = []
            st.session_state.game_state = 'game'
            st.rerun()
    
    # ステージ選択
    st.markdown("<br><h2>📋 ステージ選択</h2>", unsafe_allow_html=True)
    
    # ステージカードをグリッド表示
    for i in range(0, len(STAGES), 3):
        cols = st.columns(3)
        for j in range(3):
            stage_num = i + j + 1
            if stage_num in STAGES:
                stage_info = STAGES[stage_num]
                with cols[j]:
                    st.markdown(f"""
                    <div class="stage-card">
                        <h4>{stage_info['name']}</h4>
                        <p>単語数: {len(stage_info['words'])}個</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button(f"プレイ開始", key=f"stage_{stage_num}", use_container_width=True):
                        st.session_state.current_stage = stage_num
                        st.session_state.target_words = stage_info['words']
                        st.session_state.found_words = []
                        st.session_state.game_state = 'game'
                        st.rerun()

# ゲーム画面
elif st.session_state.game_state == 'game':
    current_stage_info = STAGES[st.session_state.current_stage]
    letters = current_stage_info['letters']
    num_letters = len(letters)
    
    # ゲームヘッダー
    st.markdown(f"""
    <div class="game-header">
        <h2 style="margin:0; text-align:center;">{current_stage_info['name']}</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # コントロールボタン
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("⬅ タイトル"):
            st.session_state.game_state = 'title'
            st.rerun()
    with col3:
        if st.button("🔄 リセット"):
            st.session_state.found_words = []
            st.rerun()
    
    # 進行状況
    progress = len(st.session_state.found_words) / len(st.session_state.target_words)
    st.progress(progress)
    st.markdown(f'<p class="progress-text">進行状況: {len(st.session_state.found_words)} / {len(st.session_state.target_words)} 単語</p>', unsafe_allow_html=True)
    
    # 目標単語の表示
    sorted_words = sorted(st.session_state.target_words)
    target_boxes_html = []
    
    for word in sorted_words:
        is_found = word in st.session_state.found_words
        boxes_html = ""
        for letter in word:
            if is_found:
                boxes_html += f'<span style="display: inline-block; width: 25px; height: 25px; border: 2px solid #4CAF50; background: #4CAF50; color: white; text-align: center; line-height: 21px; margin: 2px; font-size: 14px; font-weight: bold; border-radius: 3px;">{letter}</span>'
            else:
                boxes_html += f'<span style="display: inline-block; width: 25px; height: 25px; border: 2px solid rgba(255,255,255,0.5); background: rgba(255,255,255,0.1); text-align: center; line-height: 21px; margin: 2px; border-radius: 3px;"></span>'
        target_boxes_html.append(f'<div style="display: inline-block; margin: 8px;">{boxes_html}</div>')
    
    target_display = ' '.join(target_boxes_html)
    found_display = ', '.join(st.session_state.found_words) if st.session_state.found_words else 'なし'
    
    # 見つけた単語の表示
    if st.session_state.found_words:
        st.markdown(f"""
        <div class="found-words-display">
            <strong>✅ 見つけた単語:</strong> {found_display}
        </div>
        """, unsafe_allow_html=True)
    
    # 円形ボタンのHTML生成
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

    # HTMLゲーム部分
    full_html = f"""
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
        <style>
        body {{
            margin: 0;
            font-family: 'Arial', sans-serif;
            user-select: none;
            touch-action: none;
            overflow: hidden;
            background: transparent;
        }}
        .circle-container {{
            position: relative;
            width: 300px;
            height: 300px;
            margin: 50px auto 40px auto;
            border: 3px solid rgba(255,255,255,0.3);
            border-radius: 50%;
            background: rgba(255,255,255,0.05);
            backdrop-filter: blur(10px);
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        }}
        .circle-button {{
            position: absolute;
            width: 50px;
            height: 50px;
            border-radius: 50%;
            background: linear-gradient(135deg, #ffffff, #f0f0f0);
            color: #333;
            font-size: 20px;
            font-weight: bold;
            border: 3px solid #333;
            cursor: pointer;
            display: flex;
            justify-content: center;
            align-items: center;
            transition: all 0.3s ease;
            touch-action: none;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }}
        .circle-button.selected {{
            background: linear-gradient(135deg, #333, #000) !important;
            color: white !important;
            transform: scale(1.1);
            box-shadow: 0 6px 20px rgba(0,0,0,0.4);
        }}
        .circle-button:not(.selected):hover {{
            background: linear-gradient(135deg, #f0f0f0, #e0e0e0) !important;
            transform: scale(1.05);
        }}
        #selected-word {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            text-align: center;
            font-size: 28px;
            font-weight: bold;
            padding: 15px;
            letter-spacing: 6px;
            min-height: 50px;
            color: white;
            background: linear-gradient(135deg, rgba(0,0,0,0.8), rgba(51,51,51,0.8));
            backdrop-filter: blur(10px);
            z-index: 999;
            border-bottom: 2px solid rgba(255,255,255,0.2);
            text-shadow: 0 2px 4px rgba(0,0,0,0.5);
        }}
        #target-words {{
            position: fixed;
            top: 80px;
            left: 0;
            width: 100%;
            text-align: center;
            font-size: 14px;
            padding: 15px;
            color: white;
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            z-index: 998;
            border-bottom: 1px solid rgba(255,255,255,0.2);
        }}
        #found-words {{
            position: fixed;
            top: 140px;
            left: 0;
            width: 100%;
            text-align: center;
            font-size: 14px;
            padding: 10px;
            color: white;
            background: rgba(76, 175, 80, 0.2);
            backdrop-filter: blur(10px);
            z-index: 997;
            border-bottom: 1px solid rgba(76, 175, 80, 0.3);
            min-height: 30px;
        }}
        .success-message {{
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: linear-gradient(135deg, #4CAF50, #45a049);
            color: white;
            padding: 25px 35px;
            border-radius: 15px;
            font-size: 20px;
            font-weight: bold;
            z-index: 1000;
            opacity: 0;
            transition: all 0.4s ease;
            box-shadow: 0 10px 30px rgba(76, 175, 80, 0.4);
            border: 2px solid rgba(255,255,255,0.3);
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
            background: linear-gradient(135deg, #2196F3, #1976D2);
            color: white;
            padding: 40px 50px;
            border-radius: 20px;
            font-size: 28px;
            font-weight: bold;
            z-index: 1001;
            opacity: 0;
            transition: all 0.4s ease;
            box-shadow: 0 15px 40px rgba(33, 150, 243, 0.4);
            border: 3px solid rgba(255,255,255,0.3);
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
            pointer-events: none;
        }}
        </style>
    </head>
    <body>
    <div id="selected-word"></div>
    <div id="target-words">{target_display}</div>
    <div id="found-words">見つけた単語: {found_display}</div>
    <div id="success-message" class="success-message">🎉 正解！</div>
    <div id="complete-message" class="complete-message">🏆 ステージクリア！</div>

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
            return {{
                x: rect.left - containerRect.left + rect.width / 2,
                y: rect.top - containerRect.top + rect.height / 2
            }};
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

        function drawLine() {{
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            if (points.length < 2) return;

            ctx.beginPath();
            ctx.moveTo(points[0].x, points[0].y);
            for (let i = 1; i < points.length; i++) {{
                ctx.lineTo(points[i].x, points[i].y);
            }}
            ctx.strokeStyle = 'rgba(255,255,255,0.8)';
            ctx.lineWidth = 3;
            ctx.stroke();

            points.forEach(point => {{
                ctx.beginPath();
                ctx.arc(point.x, point.y, 3, 0, 2 * Math.PI);
                ctx.fillStyle = 'rgba(255,255,255,0.9)';
                ctx.fill();
            }});
        }}

        // マウスイベント
        function handleMouseDown(event) {{
            event.preventDefault();
            isDragging = true;
            const button = event.target.closest('.circle-button');
            if (button) {{
                selectButton(button);
            }}
        }}

        function handleMouseMove(event) {{
            event.preventDefault();
            if (!isDragging) return;
            
            const button = getButtonAtPosition(event.clientX, event.clientY);
            if (button) {{
                selectButton(button);
            }}
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
            }}
        }}

        function handleTouchMove(event) {{
            event.preventDefault();
            if (!isDragging) return;
            
            const touch = event.touches[0];
            const button = getButtonAtPosition(touch.clientX, touch.clientY);
            if (button) {{
                selectButton(button);
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

        // イベントリスナー設定
        container.addEventListener('mousedown', handleMouseDown);
        document.addEventListener('mousemove', handleMouseMove);
        document.addEventListener('mouseup', handleMouseUp);

        container.addEventListener('touchstart', handleTouchStart, {{passive: false}});
        container.addEventListener('touchmove', handleTouchMove, {{passive: false}});
        container.addEventListener('touchend', handleTouchEnd, {{passive: false}});

        // 初期化
        updateSelectedWord();

        // コンテキストメニューとテキスト選択を無効化
        document.addEventListener('contextmenu', e => e.preventDefault());
        document.addEventListener('selectstart', e => e.preventDefault());
    </script>
    </body>
    </html>
    """

    # HTMLを表示
    components.html(full_html, height=650)
    
    # ステージクリア判定
    if len(st.session_state.found_words) == len(st.session_state.target_words):
        st.markdown("""
        <div style="background: linear-gradient(135deg, #4CAF50, #45a049); 
                    color: white; padding: 2rem; border-radius: 15px; 
                    text-align: center; margin: 2rem 0;
                    box-shadow: 0 8px 32px rgba(76, 175, 80, 0.3);">
            <h2 style="margin: 0;">🏆 ステージクリア！</h2>
            <p style="margin: 0.5rem 0;">おめでとうございます！</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🔄 もう一度"):
                st.session_state.found_words = []
                st.rerun()
        
        with col2:
            if st.session_state.current_stage < len(STAGES):
                if st.button("➡️ 次のステージ"):
                    st.session_state.current_stage += 1
                    st.session_state.target_words = STAGES[st.session_state.current_stage]['words']
                    st.session_state.found_words = []
                    st.rerun()
            else:
                st.markdown('<p style="text-align: center; color: #FFD700; font-weight: bold;">🎊 全ステージクリア！</p>', unsafe_allow_html=True)
        
        with col3:
            if st.button("🏠 タイトル"):
                st.session_state.game_state = 'title'
                st.rerun()