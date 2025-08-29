import streamlit as st
import pandas as pd
import random
import math
import streamlit.components.v1 as components

# ページ設定
st.set_page_config(
    page_title="Word Connect Game",
    layout="centered",
    initial_sidebar_state="auto"
)

# カスタムCSS
st.markdown("""
<style>
/* タイトル画面のボタンスタイル */
.stButton > button {
    background-color: #333;
    color: white;
    border: 2px solid #333;
    border-radius: 8px;
    font-weight: 600;
    transition: all 0.3s ease;
    height: 50px;
}

.stButton > button:hover {
    background-color: #555;
    border-color: #555;
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}

.stButton > button:active {
    transform: translateY(0);
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}

/* プログレスバーの色調整 */
.stProgress .st-bo {
    background-color: #4CAF50;
}

/* サイドバーのスタイル調整 */
.stSidebar .stButton > button {
    background-color: #2196F3;
    border-color: #2196F3;
}

.stSidebar .stButton > button:hover {
    background-color: #1976D2;
    border-color: #1976D2;
}

/* 戻るボタンとリセットボタンのスタイル */
div[data-testid="column"] .stButton > button {
    font-size: 14px;
    padding: 0.4rem 0.8rem;
    height: 40px;
}

/* ステージタイトルの中央揃え */
.stage-title-container {
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
    width: 100% !important;
    height: 50px !important;
    text-align: center !important;
}

.stage-title {
    color: #333 !important;
    margin: 0 !important;
    padding: 0 !important;
    line-height: 1.2 !important;
    font-size: 1.8rem !important;
    font-weight: 600 !important;
    text-align: center !important;
    width: 100% !important;
}

/* SUCCESS/エラーメッセージの調整 */
.stSuccess {
    background-color: #E8F5E8;
    border-left: 4px solid #4CAF50;
}

.stWarning {
    background-color: #FFF8E1;
    border-left: 4px solid #FF9800;
}

.stError {
    background-color: #FFEBEE;
    border-left: 4px solid #F44336;
}
</style>
""", unsafe_allow_html=True)

# デフォルトの8ステージ（同じ文字も異なるものとして扱う）
def extract_unique_letters(text):
    """文字列から重複を保持した形で文字を抽出する"""
    return list(text.upper().replace(' ', ''))

DEFAULT_STAGES = {
    1: {
        'name': 'ステージ 1',
        'problem_text': 'practice',
        'letters': extract_unique_letters('practice'),
        'words': ['ACT', 'ART', 'PRICE', 'RACE', 'RICE', 'PRACTICE']
    },
    2: {
        'name': 'ステージ 2', 
        'problem_text': 'however',
        'letters': extract_unique_letters('however'),
        'words': ['HOW', 'EVER', 'WHERE', 'HOWEVER']
    },
    3: {
        'name': 'ステージ 3',
        'problem_text': 'discover',
        'letters': extract_unique_letters('discover'),
        'words': ['COVER', 'CODE', 'DIVE', 'DISCOVER']
    },
    4: {
        'name': 'ステージ 4',
        'problem_text': 'surface',
        'letters': extract_unique_letters('surface'),
        'words': ['FACE', 'ACE', 'SURF', 'CAR', 'SURFACE']
    },
    5: {
        'name': 'ステージ 5',
        'problem_text': 'suggest',
        'letters': extract_unique_letters('suggest'),
        'words': ['SET', 'GET', 'GUESS', 'GUEST', 'SUGGEST']
    },
    6: {
        'name': 'ステージ 6',
        'problem_text': 'because',
        'letters': extract_unique_letters('because'),
        'words': ['CAUSE', 'USE', 'CASE', 'SEED', 'BECAUSE']
    },
    7: {
        'name': 'ステージ 7',
        'problem_text': 'graduate',
        'letters': extract_unique_letters('graduate'),
        'words': ['GATE', 'GET', 'DATE', 'RED', 'GRADE', 'GRADUATE']
    },
    8: {
        'name': 'ステージ 8',
        'problem_text': 'attractive',
        'letters': extract_unique_letters('attractive'),
        'words': ['ACT', 'RATE', 'RARE', 'ACTIVE', 'ATTRACT', 'ATTRACTIVE']
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
if 'hints_used' not in st.session_state:
    st.session_state.hints_used = []
if 'show_hints' not in st.session_state:
    st.session_state.show_hints = {}

STAGES = DEFAULT_STAGES

# タイトル画面
if st.session_state.game_state == 'title':
    st.markdown("""
    <style>
    .title-section {
        text-align: center;
        padding: 2rem 1rem;
        margin-bottom: 2rem;
    }
    .game-title {
        font-size: 3rem;
        font-weight: 700;
        color: #333;
        margin-bottom: 1rem;
        letter-spacing: 2px;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.1);
    }
    .game-subtitle {
        font-size: 1.3rem;
        color: #555;
        margin-bottom: 2rem;
        font-weight: 400;
    }
    .game-rules {
        max-width: 600px;
        margin: 0 auto;
        padding: 2rem;
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 12px;
        text-align: left;
        margin-bottom: 1rem;
    }
    .game-rules h3 {
        color: #333;
        margin-bottom: 1rem;
        font-size: 1.2rem;
    }
    .game-rules p {
        color: #555;
        line-height: 1.6;
        margin-bottom: 0.8rem;
    }
    .stage-selection-title {
        text-align: center;
        color: #333;
        margin: 2rem 0 1.5rem 0;
        font-size: 1.8rem;
        font-weight: 600;
    }
    .stage-info {
        text-align: center;
        margin-bottom: 0.5rem;
        color: #555;
        font-weight: 500;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="title-section">
        <h1 class="game-title">RINGLISH!</h1>
        <p class="game-subtitle">文字を繋げて単語を作ろう</p>
        <div class="game-rules">
            <h3>ゲームルール</h3>
            <p>円形に配置された文字をなぞって繋げて単語を作るゲームです</p>
            <p>すべての目標単語を見つけるとステージクリア！</p>
            <p>同じ文字を重複して使うことはできません</p>
            <p>マウスまたはタッチで文字を選択してください</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # STARTボタン
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("START", key="start_button", use_container_width=True):
            st.session_state.current_stage = 1
            st.session_state.target_words = STAGES[1]['words']
            st.session_state.found_words = []
            st.session_state.hints_used = []
            st.session_state.show_hints = {}
            st.session_state.game_state = 'game'
            st.rerun()
    
    # ステージ選択
    st.markdown('<h2 class="stage-selection-title">ステージ選択</h2>', unsafe_allow_html=True)
    
    # 8つのステージを3列×3行で配置（8つ目は空白列）
    for i in range(0, 8, 3):
        cols = st.columns(3)
        for j in range(3):
            stage_num = i + j + 1
            if stage_num <= 8:
                stage_info = STAGES[stage_num]
                with cols[j]:
                    st.markdown(f'<div class="stage-info">{stage_info["name"]}</div>', unsafe_allow_html=True)
                    if st.button(f"プレイ開始", key=f"stage_{stage_num}", use_container_width=True):
                        st.session_state.current_stage = stage_num
                        st.session_state.target_words = stage_info['words']
                        st.session_state.found_words = []
                        st.session_state.hints_used = []
                        st.session_state.show_hints = {}
                        st.session_state.game_state = 'game'
                        st.rerun()

# ゲーム画面
elif st.session_state.game_state == 'game':
    current_stage_info = STAGES[st.session_state.current_stage]
    letters = current_stage_info['letters']
    num_letters = len(letters)
    
    # ヘッダー
    col1, col2, col3, col4 = st.columns([1, 3, 1, 1])
    with col1:
        if st.button("タイトルに戻る", use_container_width=True):
            st.session_state.game_state = 'title'
            st.rerun()
    with col2:
        st.markdown(f"""
        <div class="stage-title-container">
            <h2 class="stage-title">{current_stage_info['name']}</h2>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        if st.button("リセット", use_container_width=True):
            st.session_state.found_words = []
            st.session_state.hints_used = []
            st.session_state.show_hints = {}
            st.rerun()
    with col4:
        # ヒント機能はJavaScriptで処理するため、このボタンは表示しない
        st.markdown('<div style="height: 42px;"></div>', unsafe_allow_html=True)
    
    # 進行状況
    progress = len(st.session_state.found_words) / len(st.session_state.target_words)
    st.progress(progress)
    st.markdown(f"<div style='text-align: center; color: #555; font-weight: 500; margin-bottom: 1rem;'>進行状況: {len(st.session_state.found_words)} / {len(st.session_state.target_words)} 単語</div>", unsafe_allow_html=True)
    
    # 目標単語の表示（見つけた単語は文字を表示、ヒントがある場合は最初の文字を表示）
    sorted_words = sorted(st.session_state.target_words)
    target_boxes_html = []
    
    for word in sorted_words:
        is_found = word in st.session_state.found_words
        has_hint = word in st.session_state.show_hints
        boxes_html = ""
        for i, letter in enumerate(word):
            if is_found:
                # 正解済みの単語は全文字表示
                boxes_html += f'<span style="display: inline-block; width: 26px; height: 26px; border: 1px solid #333; background: white; color: #333; text-align: center; line-height: 26px; margin: 1px; font-size: 14px; font-weight: bold; border-radius: 3px; vertical-align: top;">{letter}</span>'
            elif has_hint and i == 0:
                # ヒントがある場合は最初の文字をオレンジで表示
                boxes_html += f'<span style="display: inline-block; width: 26px; height: 26px; border: 1px solid #FF9800; background: #FFF8E1; color: #FF9800; text-align: center; line-height: 26px; margin: 1px; font-size: 14px; font-weight: bold; border-radius: 3px; vertical-align: top;">{letter}</span>'
            else:
                # 通常の空白枠
                boxes_html += f'<span style="display: inline-block; width: 26px; height: 26px; border: 1px solid #ddd; background: white; text-align: center; line-height: 26px; margin: 1px; border-radius: 3px; vertical-align: top;"></span>'
        target_boxes_html.append(f'<div style="display: inline-block; margin: 6px; vertical-align: top;">{boxes_html}</div>')
    
    target_display = ''.join(target_boxes_html)
    
    # 円形ボタンのHTML生成
    button_html = ''.join([
        f'''
        <div class="circle-button" id="button_{i}"
                data-letter="{letter}"
                data-index="{i}"
                style="left: {160 + 120 * math.cos(2 * math.pi * i / num_letters - math.pi/2) - 25}px;
                       top:  {160 + 120 * math.sin(2 * math.pi * i / num_letters - math.pi/2) - 25}px;">
            {letter}
        </div>
        ''' for i, letter in enumerate(letters)
    ])

    # HTMLを表示
    components.html(f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
        <style>
        body {{
            margin: 0;
            font-family: Arial, sans-serif;
            user-select: none;
            touch-action: none;
            overflow: hidden;
            background: #fafafa;
        }}
        .circle-container {{
            position: relative;
            width: 320px;
            height: 320px;
            margin: 160px auto 40px auto;
            border: 3px solid #ddd;
            border-radius: 50%;
            background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
            box-shadow: 0 6px 12px rgba(0,0,0,0.1);
        }}
        .circle-button {{
            position: absolute;
            width: 50px;
            height: 50px;
            border-radius: 50%;
            background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
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
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            z-index: 10;
        }}
        .circle-button.selected {{
            background: linear-gradient(135deg, #2c2c2c 0%, #1a1a1a 100%) !important;
            color: white !important;
            transform: scale(1.15);
            box-shadow: 0 6px 12px rgba(0,0,0,0.3);
            border: 2px solid #1a1a1a;
            transition: all 0.1s ease;
            z-index: 10;
        }}
        .circle-button:not(.selected):hover {{
            background: linear-gradient(135deg, #f0f0f0 0%, #e9ecef 100%) !important;
            transform: scale(1.05);
            box-shadow: 0 3px 6px rgba(0,0,0,0.15);
        }}
        .circle-button.hover {{
            background: linear-gradient(135deg, #f0f0f0 0%, #e9ecef 100%) !important;
            transform: scale(1.05);
            box-shadow: 0 3px 6px rgba(0,0,0,0.15);
        }}
        #selected-word {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            text-align: center;
            font-size: 26px;
            font-weight: bold;
            padding: 12px;
            letter-spacing: 4px;
            min-height: 40px;
            color: #333;
            background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
            z-index: 999;
            border-bottom: 2px solid #e9ecef;
        }}
        #target-words {{
            position: fixed;
            top: 64px;
            left: 0;
            width: 100%;
            text-align: center;
            font-size: 16px;
            padding: 15px;
            color: #666;
            background: #f9f9f9;
            z-index: 998;
            border-bottom: 1px solid #ddd;
        }}
        .success-message {{
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
            color: white;
            padding: 20px 30px;
            border-radius: 8px;
            font-size: 18px;
            font-weight: bold;
            z-index: 1000;
            opacity: 0;
            transition: all 0.3s ease;
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
            background: linear-gradient(135deg, #2196F3 0%, #1976D2 100%);
            color: white;
            padding: 30px 40px;
            border-radius: 12px;
            font-size: 24px;
            font-weight: bold;
            z-index: 1001;
            opacity: 0;
            transition: all 0.3s ease;
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
        <div id="success-message" class="success-message">正解！</div>
        <div id="complete-message" class="complete-message">ステージクリア！</div>
        
        <!-- ヒントボタンをJavaScriptで処理 -->
        <div style="position: fixed; top: 10px; right: 10px; z-index: 1000;">
            <button onclick="showHint()" style="padding: 8px 16px; background: #333; color: white; border: none; border-radius: 4px; font-weight: bold; cursor: pointer; transition: all 0.2s ease;" onmouseover="this.style.background='#555'" onmouseout="this.style.background='#333'">ヒント</button>
        </div>

        <div class="circle-container" id="circle-container">
            <canvas id="lineCanvas" width="320" height="320"></canvas>
            {button_html}
        </div>

        <script>
        let isDragging = false;
        let selectedLetters = [];
        let selectedButtons = [];
        let points = [];
        let targetWords = {st.session_state.target_words};
        let foundWords = {st.session_state.found_words};
        let showHints = {st.session_state.show_hints};

        const selectedWordDiv = document.getElementById('selected-word');
        const targetWordsDiv = document.getElementById('target-words');
        const successMessageDiv = document.getElementById('success-message');
        const completeMessageDiv = document.getElementById('complete-message');
        const container = document.getElementById('circle-container');
        const canvas = document.getElementById('lineCanvas');
        const ctx = canvas.getContext('2d');

        function updateSelectedWord() {{
            selectedWordDiv.textContent = selectedLetters.join('');
        }}

        function updateTargetWordsDisplay() {{
            let targetBoxesHtml = [];
            let sortedWords = targetWords.slice().sort();
            
            for (let word of sortedWords) {{
                let isFound = foundWords.includes(word);
                let hasHint = showHints.hasOwnProperty(word);
                let boxesHtml = "";
                for (let i = 0; i < word.length; i++) {{
                    let letter = word[i];
                    if (isFound) {{
                        // 正解済みの単語は全文字表示
                        boxesHtml += '<span style="display: inline-block; width: 26px; height: 26px; border: 1px solid #333; background: white; color: #333; text-align: center; line-height: 26px; margin: 1px; font-size: 14px; font-weight: bold; border-radius: 3px; vertical-align: top;">' + letter + '</span>';
                    }} else if (hasHint && i === 0) {{
                        // ヒントがある場合は最初の文字をオレンジで表示
                        boxesHtml += '<span style="display: inline-block; width: 26px; height: 26px; border: 1px solid #FF9800; background: #FFF8E1; color: #FF9800; text-align: center; line-height: 26px; margin: 1px; font-size: 14px; font-weight: bold; border-radius: 3px; vertical-align: top;">' + letter + '</span>';
                    }} else {{
                        // 通常の空白枠
                        boxesHtml += '<span style="display: inline-block; width: 26px; height: 26px; border: 1px solid #ddd; background: white; text-align: center; line-height: 26px; margin: 1px; border-radius: 3px; vertical-align: top;"></span>';
                    }}
                }}
                targetBoxesHtml.push('<div style="display: inline-block; margin: 6px; vertical-align: top;">' + boxesHtml + '</div>');
            }}
            
            targetWordsDiv.innerHTML = targetBoxesHtml.join('');
        }}

        function checkCorrectWord() {{
            const currentWord = selectedLetters.join('');
            if (currentWord && targetWords.includes(currentWord) && !foundWords.includes(currentWord)) {{
                foundWords.push(currentWord);
                updateTargetWordsDisplay();
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
        
        function showHint() {{
            // まだ見つかっていない単語を取得
            let unfoundWords = targetWords.filter(word => !foundWords.includes(word));
            let availableHints = unfoundWords.filter(word => !showHints.hasOwnProperty(word));
            
            if (availableHints.length > 0) {{
                // ランダムに1つの単語を選択
                let randomIndex = Math.floor(Math.random() * availableHints.length);
                let hintWord = availableHints[randomIndex];
                showHints[hintWord] = true;
                updateTargetWordsDisplay();
            }}
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
            }}, 3000);
        }}

        function clearSelection() {{
            selectedLetters = [];
            selectedButtons.forEach(button => button.classList.remove('selected'));
            selectedButtons = [];
            points = [];
            drawLines();
            updateSelectedWord();
        }}

        function drawLines() {{
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            if (points.length > 1) {{
                ctx.strokeStyle = '#333';
                ctx.lineWidth = 3;
                ctx.lineCap = 'round';
                ctx.beginPath();
                ctx.moveTo(points[0].x, points[0].y);
                for (let i = 1; i < points.length; i++) {{
                    ctx.lineTo(points[i].x, points[i].y);
                }}
                ctx.stroke();
            }}
        }}

        // マウス/タッチイベントの処理
        function startDrag(e) {{
            e.preventDefault();
            isDragging = true;
            clearSelection();
        }}

        function handleMove(e) {{
            if (!isDragging) return;
            e.preventDefault();
            
            const rect = container.getBoundingClientRect();
            const clientX = e.touches ? e.touches[0].clientX : e.clientX;
            const clientY = e.touches ? e.touches[0].clientY : e.clientY;
            const x = clientX - rect.left;
            const y = clientY - rect.top;
            
            document.querySelectorAll('.circle-button').forEach(button => {{
                const buttonRect = button.getBoundingClientRect();
                const buttonX = buttonRect.left - rect.left + 25;
                const buttonY = buttonRect.top - rect.top + 25;
                
                if (Math.sqrt(Math.pow(x - buttonX, 2) + Math.pow(y - buttonY, 2)) < 30) {{
                    const index = parseInt(button.dataset.index);
                    if (!selectedButtons.includes(button)) {{
                        button.classList.add('selected');
                        selectedButtons.push(button);
                        selectedLetters.push(button.dataset.letter);
                        points.push({{x: buttonX, y: buttonY}});
                        drawLines();
                        updateSelectedWord();
                    }}
                }}
            }});
        }}

        function endDrag(e) {{
            if (!isDragging) return;
            e.preventDefault();
            isDragging = false;
            
            if (selectedLetters.length > 0) {{
                const isCorrect = checkCorrectWord();
                if (!isCorrect) {{
                    // 間違いの場合、少し待ってからクリア
                    setTimeout(() => {{
                        clearSelection();
                    }}, 500);
                }} else {{
                    // 正解の場合はすぐにクリア
                    clearSelection();
                }}
            }}
        }}

        // イベントリスナーの設定
        container.addEventListener('mousedown', startDrag);
        container.addEventListener('mousemove', handleMove);
        container.addEventListener('mouseup', endDrag);
        container.addEventListener('touchstart', startDrag);
        container.addEventListener('touchmove', handleMove);
        container.addEventListener('touchend', endDrag);

        // 初期化
        updateSelectedWord();
        updateTargetWordsDisplay();
        </script>
    </body>
    </html>
    """, height=800)