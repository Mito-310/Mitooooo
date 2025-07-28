import streamlit as st
import pandas as pd
import random
import math
import streamlit.components.v1 as components

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

# ファイルアップロード機能
if st.session_state.game_state == 'title':
    st.sidebar.header("問題ファイルの管理")
    
    # ファイルアップロード
    uploaded_file = st.sidebar.file_uploader(
        "新しい問題ファイルをアップロード", 
        type=['xlsx', 'xls'],
        help="問題文列と①-⑳の回答列を含むExcelファイルをアップロードしてください"
    )
    
    if uploaded_file is not None:
        try:
            # アップロードされたファイルから問題を読み込み
            df = pd.read_excel(uploaded_file)
            
            # データの確認
            st.sidebar.write("アップロードされたファイルの内容:")
            st.sidebar.dataframe(df.head())
            
            if st.sidebar.button("この問題ファイルを使用"):
                new_stages = {}
                for index, row in df.iterrows():
                    stage_num = index + 1
                    problem_text = str(row['問題文']).strip()
                    
                    # 問題文から文字を抽出
                    unique_letters = list(set(problem_text.upper().replace(' ', '')))
                    
                    # 回答列から単語を抽出
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
                STAGES = new_stages
                st.sidebar.success(f"新しい問題ファイルから{len(new_stages)}個のステージを読み込みました！")
                st.rerun()
        
        except Exception as e:
            st.sidebar.error(f"ファイル読み込みエラー: {e}")
    
    # 現在の問題ファイル情報
    st.sidebar.write(f"現在のステージ数: {len(STAGES)}")
    if st.sidebar.button("デフォルトステージに戻す"):
        st.session_state.stages = DEFAULT_STAGES
        st.rerun()

# タイトル画面
if st.session_state.game_state == 'title':
    # アイコン画像のアップロード機能（サイドバー）
    st.sidebar.header("アプリアイコン設定")
    uploaded_icon = st.sidebar.file_uploader(
        "アプリアイコンをアップロード", 
        type=['png', 'jpg', 'jpeg', 'gif'],
        help="アプリのタイトル画面に表示するアイコン画像をアップロードしてください"
    )
    
    # アイコンの表示設定を保存
    if 'app_icon' not in st.session_state:
        st.session_state.app_icon = None
    
    if uploaded_icon is not None:
        st.session_state.app_icon = uploaded_icon
        st.sidebar.success("アイコンが設定されました！")
    
    if st.sidebar.button("アイコンをリセット"):
        st.session_state.app_icon = None
        st.sidebar.info("アイコンがリセットされました")
        st.rerun()
    
    # スタイリング
    st.markdown("""
    <style>
    .title-section {
        text-align: center;
        padding: 2rem 1rem;
        margin-bottom: 2rem;
    }
    
    .app-icon {
        width: 120px;
        height: 120px;
        border-radius: 20px;
        margin: 0 auto 1.5rem auto;
        display: block;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        border: 3px solid #333;
        object-fit: cover;
    }
    
    .game-title {
        font-size: 3rem;
        font-weight: 700;
        color: #333;
        margin-bottom: 1rem;
        letter-spacing: 1px;
    }
    
    .game-subtitle {
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
    }
    
    .game-rules {
        max-width: 600px;
        margin: 0 auto;
        padding: 1.5rem;
        background: #f8f9fa;
        border-radius: 8px;
        text-align: left;
        margin-bottom: 2rem;
    }
    
    .game-rules h3 {
        color: #333;
        margin-bottom: 1rem;
        text-align: center;
        font-size: 1.1rem;
    }
    
    .game-rules ul {
        margin: 0;
        padding-left: 1.5rem;
        color: #555;
    }
    
    .game-rules li {
        margin-bottom: 0.5rem;
        line-height: 1.5;
    }
    
    .game-rules p {
        margin: 0.5rem 0;
        color: #555;
        line-height: 1.5;
    }
    
    .stage-section {
        padding: 2rem 1rem;
    }
    
    .stage-header {
        text-align: center;
        margin-bottom: 2rem;
        padding-bottom: 1rem;
        border-bottom: 1px solid #e0e0e0;
    }
    
    .stage-card {
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        background: #fafafa;
    }
    
    .stage-title {
        font-size: 1.4rem;
        font-weight: 600;
        color: #333;
        margin-bottom: 0.5rem;
    }
    
    .stage-info {
        color: #666;
        font-size: 0.9rem;
        margin-bottom: 1rem;
    }
    
    .problem-text {
        background: #e8f4f8;
        padding: 8px;
        border-radius: 4px;
        font-family: monospace;
        font-size: 0.9rem;
        margin-bottom: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # タイトルセクション
    title_content = """
    <div class="title-section">
    """
    
    # アイコンがある場合は表示
    if st.session_state.app_icon is not None:
        # 画像をbase64エンコードして埋め込み
        import base64
        from io import BytesIO
        
        # アップロードされた画像を読み込み
        image_bytes = st.session_state.app_icon.getvalue()
        image_base64 = base64.b64encode(image_bytes).decode()
        
        # 画像の形式を取得
        file_extension = st.session_state.app_icon.type.split('/')[-1]
        
        title_content += f"""
        <img src="data:image/{file_extension};base64,{image_base64}" class="app-icon" alt="App Icon">
        """
    
    title_content += """
        <h1 class="game-title">WORD CONNECT</h1>
        <p class="game-subtitle">文字を繋げて単語を作ろう</p>
        <div class="game-rules">
            <h3>ゲームルール</h3>
            <p>円形に配置された文字をドラッグして繋げて単語を作るゲームです</p>
            <p>すべての目標単語を見つけるとステージクリア！</p>
            <p>同じ文字を重複して使うことはできません</p>
            <p>マウスまたはタッチで文字を選択してください</p>
        </div>
    </div>
    """
    
    st.markdown(title_content, unsafe_allow_html=True)
    
    # STARTボタン
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("START", key="start_button", use_container_width=True):
            st.session_state.current_stage = 1
            st.session_state.target_words = STAGES[1]['words']
            st.session_state.found_words = []
            st.session_state.game_state = 'game'
            st.rerun()
    
    # ステージ選択セクション
    st.markdown("""
    <div class="stage-section">
        <div class="stage-header">
            <h2 style="color: #333; margin: 0;">ステージ選択</h2>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # ステージカードを3列で表示
    for i in range(0, len(STAGES), 3):
        cols = st.columns(3)
        for j in range(3):
            stage_num = i + j + 1
            if stage_num in STAGES:
                stage_info = STAGES[stage_num]
                with cols[j]:
                    st.markdown(f"""
                    <div class="stage-card">
                        <div class="stage-title">{stage_info['name']}</div>
                        <div class="stage-info">

                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button(f"プレイ開始", key=f"stage_{stage_num}", use_container_width=True):
                        st.session_state.current_stage = stage_num
                        st.session_state.target_words = stage_info['words']
                        st.session_state.found_words = []
                        st.session_state.game_state = 'game'
                        st.rerun()
    
    # ボタンのスタイルをカスタマイズ
    st.markdown("""
    <style>
    .stButton > button {
        background: #333 !important;
        color: white !important;
        border: none !important;
        padding: 0.75rem 1.5rem !important;
        border-radius: 4px !important;
        font-size: 1rem !important;
        font-weight: 500 !important;
        transition: all 0.2s ease !important;
        width: 100% !important;
        height: 45px !important;
    }
    
    .stButton > button:hover {
        background: #555 !important;
        transform: translateY(-1px) !important;
    }
    
    .stButton > button:active {
        transform: translateY(0px) !important;
    }
    
    /* STARTボタンのスタイル */
    .stButton[data-testid="start_button"] > button {
        background: #4CAF50 !important;
        font-size: 1.2rem !important;
        font-weight: 600 !important;
        height: 50px !important;
        border-radius: 25px !important;
        letter-spacing: 2px !important;
    }
    
    .stButton[data-testid="start_button"] > button:hover {
        background: #45a049 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# ゲーム画面
elif st.session_state.game_state == 'game':
    current_stage_info = STAGES[st.session_state.current_stage]
    letters = current_stage_info['letters']
    num_letters = len(letters)
    
    # ヘッダー
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("⬅タイトルに戻る"):
            st.session_state.game_state = 'title'
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

    # HTML + CSS + JavaScript（修正版）
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
        
        /* 選択状態のスタイル（最優先） */
        .circle-button.selected {{
            background: #333 !important;
            color: white !important;
            border: 2px solid #333 !important;
        }}
        
        /* ホバー状態（選択されていない場合のみ） */
        .circle-button:not(.selected):hover,
        .circle-button:not(.selected).hover {{
            background: #f0f0f0 !important;
        }}
        
        /* 通常状態 */
        .circle-button:not(.selected) {{
            background: white !important;
            color: #333 !important;
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
        st.success("ステージクリア！")
        
        if st.session_state.current_stage < len(STAGES):
            if st.button("次のステージへ"):
                st.session_state.current_stage += 1
                st.session_state.target_words = STAGES[st.session_state.current_stage]['words']
                st.session_state.found_words = []
                st.rerun()
        else:
            st.success("全ステージクリア！おめでとうございます！")
            if st.button("最初から始める"):
                st.session_state.current_stage = 1
                st.session_state.target_words = STAGES[1]['words']
                st.session_state.found_words = []
                st.rerun()