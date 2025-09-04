import streamlit as st
import random
import math
import json
import streamlit.components.v1 as components

# ページ設定
st.set_page_config(
    page_title="RINGLISH",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# スマホ専用CSS（縦長レイアウト最適化）
st.markdown("""
<style>
/* 全体のベーススタイル */
.main .block-container {
    padding: 0.25rem;
    max-width: 100%;
    min-height: 100vh;
}

/* スマホ専用レスポンシブ調整 */
.element-container {
    margin-bottom: 0.3rem !important;
}

.row-widget .stButton {
    margin-bottom: 0.2rem !important;
}

/* ボタンスタイル - スマホ最適化 */
.stButton > button {
    background-color: #333;
    color: white;
    border: 2px solid #333;
    border-radius: 8px;
    font-weight: 600;
    transition: all 0.3s ease;
    height: 44px;
    width: 100%;
    font-size: 15px;
    touch-action: manipulation;
}

.stButton > button:hover {
    background-color: #555;
    border-color: #555;
    transform: translateY(-1px);
    box-shadow: 0 3px 6px rgba(0,0,0,0.2);
}

.stButton > button:active {
    transform: translateY(0);
    box-shadow: 0 1px 3px rgba(0,0,0,0.2);
}

/* プライマリボタンのスタイル */
.stButton > button[kind="primary"] {
    background-color: #2196F3;
    border-color: #2196F3;
}

.stButton > button[kind="primary"]:hover {
    background-color: #1976D2;
    border-color: #1976D2;
}

/* SUCCESS/エラーメッセージの調整 */
.stSuccess {
    background-color: #E8F5E8;
    border-left: 4px solid #4CAF50;
    margin-bottom: 0.3rem;
    padding: 0.4rem;
    font-size: 14px;
}

/* タイトル画面のスタイル - スマホ最適化 */
.title-section {
    text-align: center;
    padding: 0.5rem;
    margin-bottom: 0.5rem;
}

.game-title {
    font-size: 2.2rem;
    font-weight: 700;
    color: #333;
    margin-bottom: 0.8rem;
    letter-spacing: 0.5px;
    text-shadow: 1px 1px 3px rgba(0,0,0,0.1);
}

.game-subtitle {
    font-size: 1rem;
    color: #555;
    margin-bottom: 1rem;
    font-weight: 400;
}

.game-rules {
    max-width: 100%;
    margin: 0 auto;
    padding: 1rem;
    background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
    border-radius: 8px;
    text-align: left;
    margin-bottom: 0.8rem;
}

.game-rules h3 {
    color: #333;
    margin-bottom: 0.8rem;
    font-size: 1.1rem;
}

.game-rules p {
    color: #555;
    line-height: 1.5;
    margin-bottom: 0.6rem;
    font-size: 13px;
}

.stage-selection-title {
    text-align: center;
    color: #333;
    margin: 1rem 0 0.8rem 0;
    font-size: 1.3rem;
    font-weight: 600;
}

/* ステージ選択ボタンのスタイル */
.stage-info {
    text-align: center;
    margin-bottom: 6px;
    color: #555;
    font-weight: 500;
    font-size: 12px;
}

/* ゲーム画面のヘッダー調整 */
.game-header {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 40px;
    margin-bottom: 0.3rem;
}

.game-header h2 {
    text-align: center;
    color: #333;
    margin: 0;
    line-height: 1.2;
    font-size: 1.2rem;
}

/* カラムの調整 */
.row-widget.stColumns > div {
    min-width: 0;
    flex: 1;
}

/* スペーシング調整 */
.mobile-spacing {
    margin: 0.4rem 0;
}

/* ズーム防止 */
body {
    -webkit-text-size-adjust: 100%;
    -webkit-touch-callout: none;
    -webkit-user-select: none;
}
</style>
""", unsafe_allow_html=True)

# デフォルトの問題
DEFAULT_STAGES = {
    1: {
        'name': 'ステージ 1',
        'problem_text': 'practice',
        'letters': ['P', 'R', 'A', 'C', 'T', 'I', 'C', 'E'],
        'words': ['ACT', 'AIR', 'PRICE', 'RACE', 'RICE', 'PRACTICE']
    },
    2: {
        'name': 'ステージ 2',
        'problem_text': 'however',
        'letters': ['H', 'O', 'W', 'E', 'V', 'E', 'R'],
        'words': ['HOW', 'EVER', 'WHERE', 'HOWEVER']
    },
    3: {
        'name': 'ステージ 3',
        'problem_text': 'discover',
        'letters': ['D', 'I', 'S', 'C', 'O', 'V', 'E', 'R'],
        'words': ['COVER', 'RIDE', 'DIVE', 'DISCOVER']
    },
    4: {
        'name': 'ステージ 4',
        'problem_text': 'surface',
        'letters': ['S', 'U', 'R', 'F', 'A', 'C', 'E'],
        'words': ['FACE', 'ACE', 'SURF', 'CAR', 'SURFACE']
    },
    5: {
        'name': 'ステージ 5',
        'problem_text': 'suggest',
        'letters': ['S', 'U', 'G', 'G', 'E', 'S', 'T'],
        'words': ['SET', 'GET', 'GUESS', 'GUEST', 'SUGGEST']
    },
    6: {
        'name': 'ステージ 6',
        'problem_text': 'because',
        'letters': ['B', 'E', 'C', 'A', 'U', 'S', 'E'],
        'words': ['CAUSE', 'USE', 'CASE', 'SEED', 'BECAUSE']
    },
    7: {
        'name': 'ステージ 7',
        'problem_text': 'graduate',
        'letters': ['G', 'R', 'A', 'D', 'U', 'A', 'T', 'E'],
        'words': ['GATE', 'GET', 'DATE', 'RED', 'GRADE', 'GRADUATE']
    },
    8: {
        'name': 'ステージ 8',
        'problem_text': 'attractive',
        'letters': ['A', 'T', 'T', 'R', 'A', 'C', 'T', 'I', 'V', 'E'],
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
if 'shuffled_letters' not in st.session_state:
    st.session_state.shuffled_letters = []

if 'temp_found_words' not in st.session_state:
    st.session_state.temp_found_words = []

STAGES = DEFAULT_STAGES

# タイトル画面
if st.session_state.game_state == 'title':
    
    # 画像表示（利用可能な場合）
    try:
        from PIL import Image
        import os
        import base64
        from io import BytesIO
        
        if os.path.exists('image.PNG'):
            image = Image.open('image.PNG')
            buffered = BytesIO()
            image.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            st.markdown(f'<div style="text-align: center; margin: 15px 0;"><img src="data:image/png;base64,{img_str}" width="120" style="max-width: 100%; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);"></div>', unsafe_allow_html=True)
    except:
        pass
    
    st.markdown("""
    <div class="title-section">
        <h1 class="game-title">RINGLISH!</h1>
        <div class="game-rules">
            <p>リング状に配置された文字をなぞって繋げて単語を作るゲームです</p>
            <p>すべての目標単語を見つけるとステージクリア！</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    
    # STARTボタン - スマホ専用
    col1, col2, col3 = st.columns([0.2, 1, 0.2])
    with col2:
        if st.button("START", key="start_button", use_container_width=True, type="primary"):
            st.session_state.current_stage = 1
            st.session_state.target_words = STAGES[1]['words']
            st.session_state.found_words = []
            st.session_state.temp_found_words = []
            # 文字をシャッフルして保存
            stage_letters = STAGES[1]['letters'].copy()
            random.shuffle(stage_letters)
            st.session_state.shuffled_letters = stage_letters
            st.session_state.game_state = 'game'
            st.rerun()
    
    # 区切り線
    st.markdown('<div class="mobile-spacing"></div>', unsafe_allow_html=True)
    st.markdown('<hr style="border: none; height: 1px; background: linear-gradient(90deg, transparent 0%, #ddd 50%, transparent 100%); margin: 0.8rem 0;">', unsafe_allow_html=True)
    
    # ステージ選択
    st.markdown('<h2 class="stage-selection-title">ステージ選択</h2>', unsafe_allow_html=True)
    
    # ステージ選択を2列で表示（スマホ最適化）
    for i in range(0, len(STAGES), 2):
        cols = st.columns(2)
        for j in range(2):
            stage_num = i + j + 1
            if stage_num <= len(STAGES):
                stage_info = STAGES[stage_num]
                
                with cols[j]:
                    # ステージ情報を表示
                    st.markdown(f'<div class="stage-info">{stage_info["name"]}</div>', unsafe_allow_html=True)
                    
                    # ボタン
                    button_text = "▶"
                    if st.button(button_text, key=f"stage_{stage_num}", use_container_width=True):
                        st.session_state.current_stage = stage_num
                        st.session_state.target_words = stage_info['words']
                        st.session_state.found_words = []
                        st.session_state.temp_found_words = []
                        # 文字をシャッフルして保存
                        stage_letters = stage_info['letters'].copy()
                        random.shuffle(stage_letters)
                        st.session_state.shuffled_letters = stage_letters
                        st.session_state.game_state = 'game'
                        st.rerun()
            else:
                # 空のカラム
                with cols[j]:
                    st.empty()
        
        # 行間のスペース
        if i + 2 < len(STAGES):
            st.markdown('<div style="margin: 0.3rem 0;"></div>', unsafe_allow_html=True)

# ゲーム画面
elif st.session_state.game_state == 'game':
    current_stage_info = STAGES[st.session_state.current_stage]
    
    # シャッフルされた文字配列を使用（初回の場合は作成）
    if not st.session_state.shuffled_letters or len(st.session_state.shuffled_letters) != len(current_stage_info['letters']):
        stage_letters = current_stage_info['letters'].copy()
        random.shuffle(stage_letters)
        st.session_state.shuffled_letters = stage_letters
    
    letters = st.session_state.shuffled_letters
    num_letters = len(letters)
    
    # ヘッダー（3列レイアウト）- スマホ最適化
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("戻る", key="back_to_title_header", use_container_width=True):
            st.session_state.game_state = 'title'
            st.rerun()
    with col2:
        st.markdown(f"""
        <div class="game-header">
            <h2>{current_stage_info['name']}</h2>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        # 次のステージボタン（最後のステージでない場合のみ表示）
        if st.session_state.current_stage < len(STAGES):
            if st.button("次へ", key="next_stage_header", use_container_width=True):
                st.session_state.current_stage += 1
                next_stage_info = STAGES[st.session_state.current_stage]
                st.session_state.target_words = next_stage_info['words']
                st.session_state.found_words = []
                st.session_state.temp_found_words = []
                # 新しいステージの文字をシャッフル
                stage_letters = next_stage_info['letters'].copy()
                random.shuffle(stage_letters)
                st.session_state.shuffled_letters = stage_letters
                st.rerun()
        else:
            # 最後のステージの場合は空のスペース
            st.empty()
    
    # JavaScriptから送信された正解単語をチェック
    query_params = st.query_params
    if "correct_word" in query_params:
        correct_word = query_params["correct_word"]
        if correct_word not in st.session_state.found_words:
            st.session_state.found_words.append(correct_word)
        # クエリパラメータをクリア
        st.query_params.clear()
        st.rerun()
    

    
    # 目標単語の表示（文字数→アルファベット順でソート）
    sorted_words = sorted(st.session_state.target_words, key=lambda x: (len(x), x))
    target_boxes_html = []
    
    for word in sorted_words:
        is_found = word in st.session_state.found_words
        boxes_html = ""
        for i, letter in enumerate(word):
            if is_found:
                # 正解済みの単語は全文字表示
                boxes_html += f'<span style="display: inline-block; width: 20px; height: 20px; border: 1px solid #333; background: white; color: #333; text-align: center; line-height: 20px; margin: 1px; font-size: 10px; font-weight: bold; border-radius: 3px; vertical-align: top;">{letter}</span>'
            else:
                # 通常の空白枠
                boxes_html += f'<span style="display: inline-block; width: 20px; height: 20px; border: 1px solid #ddd; background: white; text-align: center; line-height: 20px; margin: 1px; border-radius: 3px; vertical-align: top;"></span>'
        target_boxes_html.append(f'<div style="display: inline-block; margin: 3px; vertical-align: top;">{boxes_html}</div>')
    
    target_display = ''.join(target_boxes_html)
    
    # HTMLを表示（スマホ専用・縦長最適化・マウス操作のみ）
    components.html(f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no, maximum-scale=1.0, minimum-scale=1.0">
        <style>
        body {{
            margin: 0;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
            user-select: none;
            overflow-x: hidden;
            background: #fafafa;
            min-height: 100vh;
            position: relative;
            -webkit-text-size-adjust: 100%;
            -webkit-tap-highlight-color: transparent;
        }}
        
        .circle-container {{
            position: relative;
            width: 240px;
            height: 240px;
            margin: 40px auto 20px auto;
            border: 2px solid #ddd;
            border-radius: 50%;
            background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }}
        
        .circle-button {{
            position: absolute;
            width: 36px;
            height: 36px;
            border-radius: 50%;
            background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
            color: #333;
            font-size: 14px;
            font-weight: bold;
            border: 2px solid #333;
            cursor: pointer;
            display: flex;
            justify-content: center;
            align-items: center;
            transition: all 0.2s ease;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            z-index: 10;
            -webkit-touch-callout: none;
            -webkit-user-select: none;
        }}
        
        .circle-button.selected {{
            background: linear-gradient(135deg, #2c2c2c 0%, #1a1a1a 100%) !important;
            color: white !important;
            transform: scale(1.1);
            box-shadow: 0 4px 8px rgba(0,0,0,0.3);
            border: 2px solid #1a1a1a;
            transition: all 0.1s ease;
            z-index: 10;
        }}
        
        .circle-button:not(.selected):hover,
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
            font-size: 18px;
            font-weight: bold;
            padding: 8px;
            letter-spacing: 2px;
            min-height: 36px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #333;
            background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
            z-index: 999;
            border-bottom: 2px solid #e9ecef;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        
        #target-words {{
            position: fixed;
            top: 44px;
            left: 0;
            width: 100%;
            text-align: center;
            font-size: 12px;
            padding: 8px;
            color: #666;
            background: #f9f9f9;
            z-index: 998;
            border-bottom: 1px solid #ddd;
            overflow-x: auto;
            white-space: nowrap;
        }}
        
        .success-message {{
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
            color: white;
            padding: 12px 20px;
            border-radius: 8px;
            font-size: 14px;
            font-weight: bold;
            z-index: 1000;
            opacity: 0;
            transition: all 0.3s ease;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        }}
        
        .success-message.show {{
            opacity: 1;
            transform: translate(-50%, -50%) scale(1.05);
        }}
        
        .complete-message {{
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: linear-gradient(135deg, #2196F3 0%, #1976D2 100%);
            color: white;
            padding: 18px 26px;
            border-radius: 12px;
            font-size: 16px;
            font-weight: bold;
            z-index: 1001;
            opacity: 0;
            transition: all 0.3s ease;
            box-shadow: 0 6px 16px rgba(0,0,0,0.3);
        }}
        
        .complete-message.show {{
            opacity: 1;
            transform: translate(-50%, -50%) scale(1.05);
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

        <div class="circle-container" id="circle-container">
            <canvas id="lineCanvas"></canvas>
            <div id="button-container"></div>
        </div>

        <script>
        let isDragging = false;
        let selectedLetters = [];
        let selectedButtons = [];
        let points = [];
        let targetWords = {json.dumps(st.session_state.target_words)};
        let foundWords = {json.dumps(st.session_state.found_words)};
        let letters = {json.dumps(letters)};
        let numLetters = {num_letters};

        const selectedWordDiv = document.getElementById('selected-word');
        const targetWordsDiv = document.getElementById('target-words');
        const successMessageDiv = document.getElementById('success-message');
        const completeMessageDiv = document.getElementById('complete-message');
        const container = document.getElementById('circle-container');
        const buttonContainer = document.getElementById('button-container');
        const canvas = document.getElementById('lineCanvas');
        const ctx = canvas.getContext('2d');

        // 円とボタンの位置を正確に計算する関数
        function calculateButtonPositions() {{
            const containerRect = container.getBoundingClientRect();
            const containerStyle = window.getComputedStyle(container);
            const containerWidth = parseInt(containerStyle.width);
            const containerHeight = parseInt(containerStyle.height);
            
            // 円の中心点
            const centerX = containerWidth / 2;
            const centerY = containerHeight / 2;
            
            // 円の半径（ボタンが円の内側に配置されるように調整）
            const radius = Math.min(containerWidth, containerHeight) / 2 - 25; // ボタンサイズを考慮
            
            return {{
                centerX: centerX,
                centerY: centerY,
                radius: radius,
                containerWidth: containerWidth,
                containerHeight: containerHeight
            }};
        }}

        // キャンバスサイズをコンテナサイズに合わせて調整
        function resizeCanvas() {{
            const positions = calculateButtonPositions();
            
            canvas.width = positions.containerWidth;
            canvas.height = positions.containerHeight;
            canvas.style.width = positions.containerWidth + 'px';
            canvas.style.height = positions.containerHeight + 'px';
        }}

        // ボタンを作成して配置する関数
        function createButtons() {{
            const positions = calculateButtonPositions();
            buttonContainer.innerHTML = ''; // 既存のボタンをクリア
            
            for (let i = 0; i < numLetters; i++) {{
                // 各ボタンの角度を計算（12時方向から開始）
                const angle = (2 * Math.PI * i / numLetters) - Math.PI / 2;
                
                // ボタンの中心位置を計算
                const buttonCenterX = positions.centerX + positions.radius * Math.cos(angle);
                const buttonCenterY = positions.centerY + positions.radius * Math.sin(angle);
                
                // ボタン要素を作成
                const button = document.createElement('div');
                button.className = 'circle-button';
                button.id = `button_${{i}}`;
                button.dataset.letter = letters[i];
                button.dataset.index = i;
                button.textContent = letters[i];
                
                // ボタンサイズ
                const buttonSize = 36;
                
                // ボタンを中心に配置するため、左上の座標を計算
                button.style.left = (buttonCenterX - buttonSize / 2) + 'px';
                button.style.top = (buttonCenterY - buttonSize / 2) + 'px';
                
                buttonContainer.appendChild(button);
            }}
        }}

        function updateSelectedWord() {{
            selectedWordDiv.textContent = selectedLetters.join('');
        }}

        function updateTargetWordsDisplay() {{
            let targetBoxesHtml = [];
            let sortedWords = targetWords.slice().sort((a, b) => {{
                // 文字数で比較、同じなら辞書順
                if (a.length !== b.length) {{
                    return a.length - b.length;
                }}
                return a.localeCompare(b);
            }});
            
            const boxSize = 20;
            const fontSize = 10;
            
            for (let word of sortedWords) {{
                let isFound = foundWords.includes(word);
                let boxesHtml = "";
                for (let i = 0; i < word.length; i++) {{
                    let letter = word[i];
                    if (isFound) {{
                        boxesHtml += `<span style="display: inline-block; width: ${{boxSize}}px; height: ${{boxSize}}px; border: 1px solid #333; background: white; color: #333; text-align: center; line-height: ${{boxSize}}px; margin: 1px; font-size: ${{fontSize}}px; font-weight: bold; border-radius: 3px; vertical-align: top;">${{letter}}</span>`;
                    }} else {{
                        boxesHtml += `<span style="display: inline-block; width: ${{boxSize}}px; height: ${{boxSize}}px; border: 1px solid #ddd; background: white; text-align: center; line-height: ${{boxSize}}px; margin: 1px; border-radius: 3px; vertical-align: top;"></span>`;
                    }}
                }}
                targetBoxesHtml.push(`<div style="display: inline-block; margin: 2px; vertical-align: top;">${{boxesHtml}}</div>`);
            }}
            
            targetWordsDiv.innerHTML = targetBoxesHtml.join('');
        }}

        // Streamlitに正解した単語を通知する関数
        function notifyCorrectWord(word) {{
            // parent.postMessageを使ってStreamlitに通知
            window.parent.postMessage({{
                type: 'correct_word',
                word: word
            }}, '*');
        }}

        function checkCorrectWord() {{
            const currentWord = selectedLetters.join('');
            if (currentWord && targetWords.includes(currentWord) && !foundWords.includes(currentWord)) {{
                foundWords.push(currentWord);
                updateTargetWordsDisplay();
                showSuccessMessage();
                
                // Streamlitに正解を通知
                notifyCorrectWord(currentWord);
                
                if (foundWords.length === targetWords.length) {{
                    setTimeout(() => {{
                        showCompleteMessage();
                        // ステージクリア状態をStreamlitに通知
                        window.parent.postMessage({{
                            type: 'stage_complete',
                            stage: {st.session_state.current_stage}
                        }}, '*');
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

        function selectButton(button) {{
            if (!selectedButtons.includes(button)) {{
                button.classList.add('selected');
                button.classList.remove('hover');
                
                selectedLetters.push(button.dataset.letter);
                selectedButtons.push(button);
                points.push(getButtonCenterPosition(button));
                updateSelectedWord();
                drawLine();
            }}
        }}

        function clearAllSelections() {{
            document.querySelectorAll('.circle-button').forEach(button => {{
                button.classList.remove('selected');
                button.classList.remove('hover');
            }});
            selectedLetters = [];
            selectedButtons = [];
            points = [];
            updateSelectedWord();
            drawLine();
        }}

        function getButtonAtPosition(clientX, clientY) {{
            const buttons = document.querySelectorAll('.circle-button');
            let closestButton = null;
            let closestDistance = Infinity;
            
            buttons.forEach(button => {{
                if (!button.classList.contains('selected')) {{
                    button.classList.remove('hover');
                }}
            }});
            
            for (let button of buttons) {{
                const rect = button.getBoundingClientRect();
                const buttonCenterX = rect.left + rect.width / 2;
                const buttonCenterY = rect.top + rect.height / 2;
                
                const distance = Math.sqrt(
                    Math.pow(clientX - buttonCenterX, 2) + 
                    Math.pow(clientY - buttonCenterY, 2)
                );
                
                const hitRadius = 30;
                
                if (distance <= hitRadius && distance < closestDistance) {{
                    closestDistance = distance;
                    closestButton = button;
                }}
            }}
            
            if (closestButton && !closestButton.classList.contains('selected')) {{
                closestButton.classList.add('hover');
            }}
            
            return closestButton;
        }}

        function drawLine() {{
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            if (points.length < 2) return;

            const lineWidth = 3;
            const pointSize = 3;

            ctx.beginPath();
            ctx.moveTo(points[0].x, points[0].y);
            for (let i = 1; i < points.length; i++) {{
                ctx.lineTo(points[i].x, points[i].y);
            }}
            ctx.strokeStyle = '#333';
            ctx.lineWidth = lineWidth;
            ctx.lineCap = 'round';
            ctx.lineJoin = 'round';
            ctx.stroke();

            points.forEach(point => {{
                ctx.beginPath();
                ctx.arc(point.x, point.y, pointSize, 0, 2 * Math.PI);
                ctx.fillStyle = '#333';
                ctx.fill();
            }});
        }}

        // マウスイベント（スマホでもマウス操作対応）
        function handleMouseDown(event) {{
            event.preventDefault();
            isDragging = true;
            clearAllSelections();
            
            const button = getButtonAtPosition(event.clientX, event.clientY);
            if (button) {{
                selectButton(button);
            }}
        }}

        function handleMouseMove(event) {{
            event.preventDefault();
            
            if (isDragging) {{
                const button = getButtonAtPosition(event.clientX, event.clientY);
                if (button) {{
                    selectButton(button);
                }}
            }} else {{
                getButtonAtPosition(event.clientX, event.clientY);
            }}
        }}

        function handleMouseUp(event) {{
            event.preventDefault();
            if (isDragging) {{
                isDragging = false;
                const isCorrect = checkCorrectWord();
                
                setTimeout(() => {{
                    clearAllSelections();
                }}, isCorrect ? 1000 : 200);
            }}
            document.querySelectorAll('.circle-button').forEach(button => {{
                button.classList.remove('hover');
            }});
        }}

        // 初期化とリサイズ処理
        function initialize() {{
            createButtons();
            resizeCanvas();
            updateSelectedWord();
            updateTargetWordsDisplay();
        }}

        // マウスイベントリスナーの設定
        document.addEventListener('mousedown', handleMouseDown);
        document.addEventListener('mousemove', handleMouseMove);
        document.addEventListener('mouseup', handleMouseUp);

        // リサイズイベント
        window.addEventListener('resize', () => {{
            initialize();
        }});

        // 初期化
        initialize();

        // 右クリックメニューと選択を無効化
        document.addEventListener('contextmenu', e => e.preventDefault());
        document.addEventListener('selectstart', e => e.preventDefault());
        
        // モバイルブラウザでのズームを防止
        document.addEventListener('gesturestart', e => e.preventDefault());
        document.addEventListener('gesturechange', e => e.preventDefault());
        document.addEventListener('gestureend', e => e.preventDefault());
        </script>
    </body>
    </html>
    """, height=420)

    # JavaScriptからのメッセージを受信するためのプレースホルダー
    message_placeholder = st.empty()
    
    # postMessageを監視するためのJavaScript
    components.html("""
    <script>
    window.addEventListener('message', function(event) {
        if (event.data.type === 'correct_word') {
            // URLパラメータを使ってStreamlitに正解した単語を通知
            const currentUrl = new URL(window.location);
            currentUrl.searchParams.set('correct_word', event.data.word);
            window.location.href = currentUrl.toString();
        }
        if (event.data.type === 'stage_complete') {
            // ステージクリア通知（特別な処理は不要）
            console.log('Stage completed:', event.data.stage);
        }
    });
    </script>
    """, height=0)
    
    # ステージクリア状態の確認
    stage_completed = len(st.session_state.found_words) == len(st.session_state.target_words)
    
    if stage_completed:
        st.success("ステージクリア！")
        col1, col2, col3 = st.columns([0.2, 1, 0.2])
        with col2:
            if st.session_state.current_stage < len(STAGES):
                if st.button("次のステージへ", key="next_stage_main", use_container_width=True, type="primary"):
                    st.session_state.current_stage += 1
                    next_stage_info = STAGES[st.session_state.current_stage]
                    st.session_state.target_words = next_stage_info['words']
                    st.session_state.found_words = []
                    st.session_state.temp_found_words = []
                    # 新しいステージの文字をシャッフル
                    stage_letters = next_stage_info['letters'].copy()
                    random.shuffle(stage_letters)
                    st.session_state.shuffled_letters = stage_letters
                    st.rerun()
            else:
                st.balloons()
                st.success("全ステージクリア！おめでとうございます！")
                if st.button("タイトルに戻る", key="back_to_title", use_container_width=True, type="primary"):
                    st.session_state.game_state = 'title'
                    st.rerun()