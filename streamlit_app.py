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
if 'letter_order' not in st.session_state:
    st.session_state.letter_order = []
if 'is_lowercase' not in st.session_state:
    st.session_state.is_lowercase = False

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
    # スタイリング
    st.markdown("""
    <style>
    .title-section {
        text-align: center;
        padding: 3rem 1rem;
        margin-bottom: 2rem;
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
    </style>
    """, unsafe_allow_html=True)
    
    # タイトルセクション
    st.markdown("""
    <div class="title-section">
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
    """, unsafe_allow_html=True)
    
    # STARTボタン
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("START", key="start_button", use_container_width=True):
            st.session_state.current_stage = 1
            st.session_state.target_words = STAGES[1]['words']
            st.session_state.found_words = []
            st.session_state.letter_order = list(range(len(STAGES[1]['letters'])))
            st.session_state.is_lowercase = False
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
                            文字数: {len(stage_info['letters'])}<br>
                            単語数: {len(stage_info['words'])}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button(f"プレイ開始", key=f"stage_{stage_num}", use_container_width=True):
                        st.session_state.current_stage = stage_num
                        st.session_state.target_words = stage_info['words']
                        st.session_state.found_words = []
                        st.session_state.letter_order = list(range(len(stage_info['letters'])))
                        st.session_state.is_lowercase = False
                        st.session_state.game_state = 'game'
                        st.rerun()

# ゲーム画面
elif st.session_state.game_state == 'game':
    current_stage_info = STAGES[st.session_state.current_stage]
    letters = current_stage_info['letters']
    num_letters = len(letters)
    
    # 文字順序の初期化
    if not st.session_state.letter_order or len(st.session_state.letter_order) != num_letters:
        st.session_state.letter_order = list(range(num_letters))
    
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
    
    # サイドバーでシャッフルと文字切り替え
    with st.sidebar:
        if st.button("シャッフル"):
            random.shuffle(st.session_state.letter_order)
            st.rerun()
        
        if st.button("大文字⇄小文字"):
            st.session_state.is_lowercase = not st.session_state.is_lowercase
            st.rerun()
        
        # ヒント機能
        st.subheader("ヒント")
        st.write(f"問題文: {current_stage_info['problem_text']}")
        
        # 単語リストの表示（折りたたみ式）
        with st.expander("単語リストを表示"):
            st.write("目標単語:")
            for word in sorted(st.session_state.target_words):
                status = "✅" if word in st.session_state.found_words else "⬜"
                st.write(f"{status} {word}")
    
    # 進行状況
# セッションステートから取得（安全に）
found_words = st.session_state.get("found_words", [])
target_words = st.session_state.get("target_words", [])

# 長さの取得
num_found = len(found_words)
num_total = len(target_words)

# 安全な進捗値の計算
if num_total > 0:
    progress = min(num_found / num_total, 1.0)  # 1.0 を超えないように制限
else:
    progress = 0.0  # デフォルト

# 表示
st.progress(progress)
st.write(f"進行状況: {num_found} / {num_total} 単語")

    
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
found_display = ', '.join(str(word) for word in st.session_state.get("found_words", []))
    
    # 円形に並べるボタンのHTMLを生成（シャッフル順序を適用）
display_letters = []
for i in st.session_state.letter_order:
        letter = letters[i]
        display_letter = letter.lower() if st.session_state.is_lowercase else letter
        display_letters.append(display_letter)
    
button_html = ''.join([
        f'''
        <div class="circle-button" id="button_{i}"
                data-letter="{letter}"
                data-index="{i}"
                style="left: {150 + 120 * math.cos(2 * math.pi * i / num_letters - math.pi/2) - 25}px;
                       top:  {150 + 120 * math.sin(2 * math.pi * i / num_letters - math.pi/2) - 25}px;">
            {letter}
        </div>
        ''' for i, letter in enumerate(display_letters)
    ])

    # 単語を見つけた時のStreamlit側での処理
if st.session_state.found_words and len(st.session_state.found_words) == len(st.session_state.target_words):
        st.success("ステージクリア！おめでとうございます！")
        
        # 次のステージボタン
        next_stage = st.session_state.current_stage + 1
        if next_stage in STAGES:
            if st.button(f"次のステージ ({next_stage}) へ進む"):
                st.session_state.current_stage = next_stage
                st.session_state.target_words = STAGES[next_stage]['words']
                st.session_state.found_words = []
                st.session_state.letter_order = list(range(len(STAGES[next_stage]['letters'])))
                st.rerun()
    
    # JavaScriptとHTMLの生成（f-stringの中括弧問題を回避）
js_target_words = str(st.session_state.target_words)
js_found_words = str(st.session_state.found_words)
js_is_lowercase = str(st.session_state.is_lowercase).lower()
    
html_content = f"""
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
            background: #f5f5f5;
        }}
        .circle-container {{
            position: relative;
            width: 300px;
            height: 300px;
            margin: 20px auto;
            border: 3px solid #333;
            border-radius: 50%;
            touch-action: none;
            background: linear-gradient(135deg, #f9f9f9, #e0e0e0);
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }}
        .circle-button {{
            position: absolute;
            width: 50px;
            height: 50px;
            border-radius: 50%;
            background: linear-gradient(135deg, #ffffff, #f0f0f0);
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
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .circle-button.selected {{
            background: linear-gradient(135deg, #333, #555);
            color: white;
            transform: scale(1.1);
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }}
        .circle-button:hover {{
            background: linear-gradient(135deg, #e0e0e0, #d0d0d0);
            transform: scale(1.05);
        }}
        .circle-button.hover {{
            background: linear-gradient(135deg, #e0e0e0, #d0d0d0);
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
            user-select: none;
            letter-spacing: 6px;
            min-height: 50px;
            color: #333;
            background: linear-gradient(135deg, #fff, #f9f9f9);
            z-index: 999;
            border-bottom: 2px solid #ccc;
            touch-action: none;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        #target-words {{
            position: fixed;
            top: 70px;
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
            box-shadow: 0 8px 16px rgba(0,0,0,0.2);
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
            font-size: 26px;
            font-weight: bold;
            z-index: 1001;
            opacity: 0;
            transition: all 0.4s ease;
            box-shadow: 0 12px 24px rgba(0,0,0,0.3);
            text-align: center;
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
        .instruction {{
            text-align: center;
            color: #666;
            font-size: 14px;
            margin: 10px 0;
        }}
        </style>
    </head>
    <body>
    <div id="selected-word">単語を作ってください</div>
    <div id="target-words">{target_display}</div>
    <div id="found-words">見つけた単語: {found_display}</div>
    <div id="success-message" class="success-message">正解！</div>
    <div id="complete-message" class="complete-message">clear!<br>おめでとうございます！</div>

    <div class="instruction">文字をドラッグして単語を作ってください</div>
    
    <div class="circle-container" id="circle-container">
        {button_html}
        <canvas id="lineCanvas" width="300" height="300"></canvas>
    </div>

    <script>
    
    </script>
    </body>
    </html>

    <style>
    """
st.markdown("""
    .success-message {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background: linear-gradient(#4CAF50, #45a049);
        color: white;
        padding: 25px 35px;
        border-radius: 15px;
        font-size: 20px;
        font-weight: bold;
        z-index: 1000;
        opacity: 0;
        transition: all 0.4s ease;
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
    }
    .success-message.show {
        opacity: 1;
        transform: translate(-50%, -50%) scale(1.1);
    }
    .complete-message {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background: linear-gradient(135deg, #2196F3, #1976D2);
        color: white;
        padding: 40px 50px;
        border-radius: 20px;
        font-size: 26px;
        font-weight: bold;
        z-index: 1001;
        opacity: 0;
        transition: all 0.4s ease;
        box-shadow: 0 12px 24px rgba(0,0,0,0.3);
        text-align: center;
    }
    .complete-message.show {
        opacity: 1;
        transform: translate(-50%, -50%) scale(1.1);
    }
    canvas {
        position: absolute;
        top: 0;
        left: 0;
        z-index: 1;
        touch-action: none;
        pointer-events: none;
    }
    .instruction {
        text-align: center;
        color: #666;
        font-size: 14px;
        margin: 10px 0;
    }

""", unsafe_allow_html=True)


"""</head>
    <body>
    <div id="selected-word">単語を作ってください</div>
    <div id="target-words">{target_display}</div>
    <div id="found-words">見つけた単語: {found_display}</div>
    <div id="success-message" class="success-message">正解！</div>
    <div id="complete-message" class="complete-message">clear!<br>おめでとうございます！</div>

    <div class="instruction">文字をドラッグして単語を作ってください</div>
    
    <div class="circle-container" id="circle-container">
        {button_html}
        <canvas id="lineCanvas" width="300" height="300"></canvas>
    </div>

    <script>
        let isDragging = false;
        let selectedLetters = [];
        let selectedButtons = [];
        let points = [];
        let targetWords = {js_target_words};
        let foundWords = {js_found_words};
        let currentHoverButton = null;
        let isLowercase = {js_is_lowercase};

        const selectedWordDiv = document.getElementById('selected-word');
        const targetWordsDiv = document.getElementById('target-words');
        const foundWordsDiv = document.getElementById('found-words');
        const successMessageDiv = document.getElementById('success-message');
        const completeMessageDiv = document.getElementById('complete-message');
        const container = document.getElementById('circle-container');
        const canvas = document.getElementById('lineCanvas');
        const ctx = canvas.getContext('2d');

        function updateSelectedWord() {{
            selectedWordDiv.textContent = selectedLetters.length > 0 ? selectedLetters.join('') : '単語を作ってください';
        }}

        function checkCorrectWord() {{
            const currentWord = selectedLetters.join('').toUpperCase();
            if (currentWord && targetWords.includes(currentWord) && !foundWords.includes(currentWord)) {{
                foundWords.push(currentWord);
                foundWordsDiv.textContent = '見つけた単語: ' + foundWords.join(', ');
                showSuccessMessage();
                
                // Streamlitに単語発見を通知（ページリロードを促す）
                setTimeout(() => {{
                    window.parent.postMessage({{
                        type: 'streamlit:setComponentValue',
                        value: currentWord
                    }}, '*');
                }}, 500);
                
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
                // ステージクリア後にStreamlitに通知
                window.parent.postMessage({{
                    type: 'streamlit:setComponentValue',
                    value: 'STAGE_COMPLETE'
                }}, '*');
            }}, 4000);
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
            const containerRect = container.getBoundingClientRect();
            
            for (let button of buttons) {{
                const buttonLeft = parseFloat(button.style.left);
                const buttonTop = parseFloat(button.style.top);
                const relativeX = x - containerRect.left;
                const relativeY = y - containerRect.top;
                
                if (relativeX >= buttonLeft && relativeX <= buttonLeft + 50 &&
                    relativeY >= buttonTop && relativeY <= buttonTop + 50) {{
                    return button;
                }}
            }}
            return null;
        }}

        function drawLine() {{
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            
            if (points.length > 1) {{
                ctx.strokeStyle = '#333';
                ctx.lineWidth = 3;
                ctx.lineCap = 'round';
                
                ctx.beginPath();
                ctx.moveTo(points[0].x, points[0].y);
                for (let i = 1; i < points.length; i++) {
                    ctx.lineTo(points[i].x, points[i].y);
                }
                ctx.stroke();
            }
        }

        function handleHover(button) {
            if (isDragging && !selectedButtons.includes(button)) {
                if (currentHoverButton && currentHoverButton !== button) {
                    currentHoverButton.classList.remove('hover');
                }
                button.classList.add('hover');
                currentHoverButton = button;
            }
        }

        function clearHover() {
            if (currentHoverButton) {
                currentHoverButton.classList.remove('hover');
                currentHoverButton = null;
            }
        }

        // マウスイベント
        container.addEventListener('mousedown', (e) => {
            e.preventDefault();
            const button = getButtonAtPosition(e.clientX, e.clientY);
            if (button) {
                isDragging = true;
                resetSelection();
                selectButton(button);
            }
        });

        container.addEventListener('mousemove', (e) => {
            if (isDragging) {
                e.preventDefault();
                const button = getButtonAtPosition(e.clientX, e.clientY);
                if (button) {
                    handleHover(button);
                    if (!selectedButtons.includes(button)) {
                        selectButton(button);
                        clearHover();
                    }
                } else {
                    clearHover();
                }
            }
        });

        container.addEventListener('mouseup', (e) => {
            if (isDragging) {
                e.preventDefault();
                isDragging = false;
                clearHover();
                
                if (selectedLetters.length > 0) {
                    const found = checkCorrectWord();
                    if (!found) {
                        // 間違った単語の場合、短時間後にリセット
                        setTimeout(() => {
                            resetSelection();
                        }, 1000);
                    } else {
                        resetSelection();
                    }
                }
            }
        });

        // タッチイベント
        container.addEventListener('touchstart', (e) => {
            e.preventDefault();
            const touch = e.touches[0];
            const button = getButtonAtPosition(touch.clientX, touch.clientY);
            if (button) {
                isDragging = true;
                resetSelection();
                selectButton(button);
            }
        }, { passive: false });

        container.addEventListener('touchmove', (e) => {
            if (isDragging) {
                e.preventDefault();
                const touch = e.touches[0];
                const button = getButtonAtPosition(touch.clientX, touch.clientY);
                if (button) {
                    handleHover(button);
                    if (!selectedButtons.includes(button)) {
                        selectButton(button);
                        clearHover();
                    }
                } else {
                    clearHover();
                }
            }
        }, { passive: false });

        container.addEventListener('touchend', (e) => {
            if (isDragging) {
                e.preventDefault();
                isDragging = false;
                clearHover();
                
                if (selectedLetters.length > 0) {
                    const found = checkCorrectWord();
                    if (!found) {
                        // 間違った単語の場合、短時間後にリセット
                        setTimeout(() => {
                            resetSelection();
                        }, 1000);
                    } else {
                        resetSelection();
                    }
                }
            }
        }, { passive: false });

        // ページ外でのマウス/タッチ終了を処理
        document.addEventListener('mouseup', () => {
            if (isDragging) {
                isDragging = false;
                clearHover();
                if (selectedLetters.length > 0) {
                    const found = checkCorrectWord();
                    if (!found) {
                        setTimeout(() => {
                            resetSelection();
                        }, 1000);
                    } else {
                        resetSelection();
                    }
                }
            }
        });

        document.addEventListener('touchend', () => {
            if (isDragging) {
                isDragging = false;
                clearHover();
                if (selectedLetters.length > 0) {
                    const found = checkCorrectWord();
                    if (!found) {
                        setTimeout(() => {
                            resetSelection();
                        }, 1000);
                    } else {
                        resetSelection();
                    }
                }
            }
        });

        // キーボードイベント（ESCでリセット）
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                resetSelection();
            }
        });

        // 初期化
        updateSelectedWord();
        drawLine();

    </style>
    </script>
    </body>
    </html>
    """

    # HTML コンポーネントを表示
found_word = components.html(html_content, height=550, scrolling=False)
    
    # 単語が見つかった場合の処理
if found_word and found_word != "STAGE_COMPLETE" and found_word not in st.session_state.found_words:
    st.session_state.found_words.append(found_word)
    st.rerun()
    
    # ステージクリアの処理
if found_word == "STAGE_COMPLETE":
    st.rerun()