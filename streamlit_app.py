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

# Excelファイルから問題を読み込む関数
@st.cache_data
def load_problems_from_excel(file_path):
    """Excelファイルから問題を読み込む"""
    try:
        df = pd.read_excel(file_path)
        problems = {}
        
        # 各行を処理して問題を作成
        for index, row in df.iterrows():
            stage_num = index + 1
            problem_text = str(row['問題文']).strip()
            
            # 問題文から文字を抽出（重複を除去）
            unique_letters = list(set(problem_text.upper().replace(' ', '')))
            
            # ①-⑳の列から単語を抽出
            words = []
            for col in df.columns[1:]:  # 問題文以外の列
                if pd.notna(row[col]):
                    word = str(row[col]).strip().upper()
                    if word and word not in words:
                        words.append(word)
            
            problems[stage_num] = {
                'name': f'ステージ {stage_num}',
                'problem_text': problem_text,
                'letters': unique_letters,
                'words': words
            }
        
        return problems
    except Exception as e:
        st.error(f"Excelファイルの読み込みエラー: {e}")
        return None

# デフォルトの問題（Excelファイルが読み込めない場合の備え）
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
if 'stages' not in st.session_state:
    st.session_state.stages = None

# Excelファイルから問題を読み込み
if st.session_state.stages is None:
    try:
        loaded_stages = load_problems_from_excel('Book.xlsx')
        if loaded_stages:
            st.session_state.stages = loaded_stages
            st.success(f"Excelファイルから{len(loaded_stages)}個のステージを読み込みました")
        else:
            st.session_state.stages = DEFAULT_STAGES
            st.warning("Excelファイルの読み込みに失敗しました。デフォルトステージを使用します。")
    except:
        st.session_state.stages = DEFAULT_STAGES
        st.warning("Book.xlsxが見つかりません。デフォルトステージを使用します。")

STAGES = st.session_state.stages

# ファイルアップロード機能（タイトル画面でのみ表示）
if st.session_state.game_state == 'title':
    st.sidebar.header("問題ファイルの管理")
    
    uploaded_file = st.sidebar.file_uploader(
        "新しい問題ファイルをアップロード", 
        type=['xlsx', 'xls'],
        help="問題文列と①-⑳の回答列を含むExcelファイルをアップロードしてください"
    )
    
    if uploaded_file is not None:
        try:
            df = pd.read_excel(uploaded_file)
            st.sidebar.write("アップロードされたファイルの内容:")
            st.sidebar.dataframe(df.head())
            
            if st.sidebar.button("この問題ファイルを使用"):
                new_stages = {}
                for index, row in df.iterrows():
                    stage_num = index + 1
                    problem_text = str(row['問題文']).strip()
                    unique_letters = list(set(problem_text.upper().replace(' ', '')))
                    
                    words = []
                    for col in df.columns[1:]:
                        if pd.notna(row[col]):
                            word = str(row[col]).strip().upper()
                            if word and word not in words:
                                words.append(word)
                    
                    new_stages[stage_num] = {
                        'name': f'ステージ {stage_num}',
                        'problem_text': problem_text,
                        'letters': unique_letters,
                        'words': words
                    }
                
                st.session_state.stages = new_stages
                st.sidebar.success(f"新しい問題ファイルから{len(new_stages)}個のステージを読み込みました！")
                st.rerun()
        
        except Exception as e:
            st.sidebar.error(f"ファイル読み込みエラー: {e}")
    
    st.sidebar.write(f"現在のステージ数: **{len(STAGES)}**")
    if st.sidebar.button("デフォルトステージに戻す"):
        st.session_state.stages = DEFAULT_STAGES
        st.rerun()

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
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
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
            st.markdown(f'<div style="text-align: center; margin: 20px 0;"><img src="data:image/png;base64,{img_str}" width="200" style="max-width: 100%; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);"></div>', unsafe_allow_html=True)
    except:
        pass
    
    st.markdown("""
    <div class="title-section">
        <h1 class="game-title">WORD CONNECT</h1>
        <p class="game-subtitle">文字を繋げて単語を作ろう</p>
        <div class="game-rules">
            <h3>ゲームルール</h3>
            <p> 円形に配置された文字をドラッグして繋げて単語を作るゲームです</p>
            <p> すべての目標単語を見つけるとステージクリア！</p>
            <p> 同じ文字を重複して使うことはできません</p>
            <p> マウスまたはタッチで文字を選択してください</p>
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
            st.session_state.game_state = 'game'
            st.rerun()
    
    # ステージ選択
    st.markdown('<h2 class="stage-selection-title">ステージ選択</h2>', unsafe_allow_html=True)
    
    for i in range(0, len(STAGES), 3):
        cols = st.columns(3)
        for j in range(3):
            stage_num = i + j + 1
            if stage_num in STAGES:
                stage_info = STAGES[stage_num]
                with cols[j]:
                    st.markdown(f'<div class="stage-info">{stage_info["name"]}</div>', unsafe_allow_html=True)
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
    
    # ヘッダー
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("タイトルに戻る"):
            st.session_state.game_state = 'title'
            st.rerun()
    with col2:
        st.markdown(f"<h2 style='text-align: center; color: #333; margin: 0;'>{current_stage_info['name']}</h2>", unsafe_allow_html=True)
    with col3:
        if st.button("リセット"):
            st.session_state.found_words = []
            st.rerun()
    
    # 進行状況
    progress = len(st.session_state.found_words) / len(st.session_state.target_words)
    st.progress(progress)
    st.markdown(f"<div style='text-align: center; color: #555; font-weight: 500; margin-bottom: 1rem;'>進行状況: {len(st.session_state.found_words)} / {len(st.session_state.target_words)} 単語</div>", unsafe_allow_html=True)
    
    # 目標単語の表示（見つけた単語は緑で表示）
    sorted_words = sorted(st.session_state.target_words)
    target_boxes_html = []
    
    for word in sorted_words:
        is_found = word in st.session_state.found_words
        boxes_html = ""
        for letter in word:
            if is_found:
                boxes_html += f'<span style="display: inline-block; width: 26px; height: 26px; border: 1px solid #4CAF50; background: #4CAF50; color: white; text-align: center; line-height: 24px; margin: 1px; font-size: 14px; font-weight: bold; border-radius: 3px;">{letter}</span>'
            else:
                boxes_html += f'<span style="display: inline-block; width: 26px; height: 26px; border: 1px solid #ddd; background: white; text-align: center; line-height: 24px; margin: 1px; border-radius: 3px;"></span>'
        target_boxes_html.append(f'<div style="display: inline-block; margin: 6px;">{boxes_html}</div>')
    
    target_display = ' '.join(target_boxes_html)
    
    # 円形ボタンのHTML生成
    button_html = ''.join([
        f'''
        <div class="circle-button" id="button_{i}"
                data-letter="{letter}"
                data-index="{i}"
                style="left: {160 + 130 * math.cos(2 * math.pi * i / num_letters - math.pi/2) - 25}px;
                       top:  {160 + 130 * math.sin(2 * math.pi * i / num_letters - math.pi/2) - 25}px;">
            {letter}
        </div>
        ''' for i, letter in enumerate(letters)
    ])

    # HTMLを表示
    components.html(full_html, height=600)
    
    # ステージクリア判定
    if len(st.session_state.found_words) == len(st.session_state.target_words):
        st.success("ステージクリア！")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("もう一度プレイ"):
                st.session_state.found_words = []
                st.rerun()
        
        with col2:
            if st.session_state.current_stage < len(STAGES):
                if st.button("→次のステージ"):
                    st.session_state.current_stage += 1
                    st.session_state.target_words = STAGES[st.session_state.current_stage]['words']
                    st.session_state.found_words = []
                    st.rerun()
            else:
                st.markdown("<div style='text-align: center; color: #4CAF50; font-weight: bold; font-size: 18px;'>全ステージクリア！</div>", unsafe_allow_html=True)
        
        with col3:
            if st.button("タイトルに戻る"):
                st.session_state.game_state = 'title'
                st.rerun()

    full_html = f"""<!DOCTYPE html>
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
            width: 300px;
            height: 300px;
            margin: 180px auto 40px auto;
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
        }}
        .circle-button.selected {{
            background: linear-gradient(135deg, #333 0%, #555 100%) !important;
            color: white !important;
            transform: scale(1.1);
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }}
        .circle-button:not(.selected):hover {{
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
            box-shadow: 0 6px 12px rgba(76, 175, 80, 0.3);
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
            box-shadow: 0 8px 16px rgba(33, 150, 243, 0.3);
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
                let boxesHtml = "";
                for (let letter of word) {{
                    if (isFound) {{
                        boxesHtml += '<span style="display: inline-block; width: 26px; height: 26px; border: 1px solid #4CAF50; background: #4CAF50; color: white; text-align: center; line-height: 24px; margin: 1px; font-size: 14px; font-weight: bold; border-radius: 3px;">' + letter + '</span>';
                    }} else {{
                        boxesHtml += '<span style="display: inline-block; width: 26px; height: 26px; border: 1px solid #ddd; background: white; text-align: center; line-height: 24px; margin: 1px; border-radius: 3px;"></span>';
                    }}
                }}
                targetBoxesHtml.push('<div style="display: inline-block; margin: 6px;">' + boxesHtml + '</div>');
            }}
            
            targetWordsDiv.innerHTML = targetBoxesHtml.join(' ');
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
            ctx.strokeStyle = '#333';
            ctx.lineWidth = 3;
            ctx.stroke();

            points.forEach(point => {{
                ctx.beginPath();
                ctx.arc(point.x, point.y, 3, 0, 2 * Math.PI);
                ctx.fillStyle = '#333';
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

        <script>
        let isDragging = false;
        let selectedLetters = [];
        let selectedButtons = [];
        let points = [];
        let targetWords = {st.session_state.target_words};
        let foundWords = {st.session_state.found_words};

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
                let boxesHtml = "";
                for (let letter of word) {{
                    if (isFound) {{
                        boxesHtml += '<span style="display: inline-block; width: 26px; height: 26px; border: 1px solid #4CAF50; background: #4CAF50; color: white; text-align: center; line-height: 24px; margin: 1px; font-size: 14px; font-weight: bold; border-radius: 3px;">' + letter + '</span>';
                    }} else {{
                        boxesHtml += '<span style="display: inline-block; width: 26px; height: 26px; border: 1px solid #ddd; background: white; text-align: center; line-height: 24px; margin: 1px; border-radius: 3px;"></span>';
                    }}
                }}
                targetBoxesHtml.push('<div style="display: inline-block; margin: 6px;">' + boxesHtml + '</div>');
            }}
            
            targetWordsDiv.innerHTML = targetBoxesHtml.join(' ');
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
            ctx.strokeStyle = '#333';
            ctx.lineWidth = 3;
            ctx.stroke();

            points.forEach(point => {{
                ctx.beginPath();
                ctx.arc(point.x, point.y, 3, 0, 2 * Math.PI);
                ctx.fillStyle = '#333';
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
        updateTargetWordsDisplay();

        // コンテキストメニューとテキスト選択を無効化
        document.addEventListener('contextmenu', e => e.preventDefault());
        document.addEventListener('selectstart', e => e.preventDefault());
        </script>
    </body>
    </html>"""

    # HTML