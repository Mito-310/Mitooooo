import streamlit as st
import random
import math
import json
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

/* シャッフルボタン専用のスタイル */
.shuffle-button > button {
    background-color: #333 !important;
    color: white !important;
    border: 2px solid #333 !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
    height: 50px !important;
}

.shuffle-button > button:hover {
    background-color: #555 !important;
    border-color: #555 !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2) !important;
}

.shuffle-button > button:active {
    transform: translateY(0) !important;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2) !important;
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

/* クリア済みステージボタンのスタイル */
.cleared-stage > button {
    background-color: #4CAF50 !important;
    border-color: #4CAF50 !important;
    color: white !important;
}

.cleared-stage > button:hover {
    background-color: #45a049 !important;
    border-color: #45a049 !important;
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
if 'hints_used' not in st.session_state:
    st.session_state.hints_used = []
if 'show_hints' not in st.session_state:
    st.session_state.show_hints = {}
if 'shuffled_letters' not in st.session_state:
    st.session_state.shuffled_letters = []
if 'cleared_stages' not in st.session_state:
    st.session_state.cleared_stages = set()

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
            st.session_state.hints_used = []
            st.session_state.show_hints = {}
            # 文字をシャッフルして保存
            stage_letters = STAGES[1]['letters'].copy()
            random.shuffle(stage_letters)
            st.session_state.shuffled_letters = stage_letters
            st.session_state.game_state = 'game'
            st.rerun()
    
    # 区切り線
    st.markdown('<hr style="border: none; height: 2px; background: linear-gradient(90deg, transparent 0%, #ddd 50%, transparent 100%); margin: 2rem 0;">', unsafe_allow_html=True)
    
    # ステージ選択
    st.markdown('<h2 class="stage-selection-title">ステージ選択</h2>', unsafe_allow_html=True)
    
    for i in range(0, len(STAGES), 3):
        cols = st.columns(3)
        for j in range(3):
            stage_num = i + j + 1
            if stage_num in STAGES:
                stage_info = STAGES[stage_num]
                is_cleared = stage_num in st.session_state.cleared_stages
                with cols[j]:
                    st.markdown(f'<div class="stage-info">{stage_info["name"]}</div>', unsafe_allow_html=True)
                    
                    # クリア済みの場合は緑色のボタンにチェックマークを追加
                    if is_cleared:
                        button_text = "✓ CLEAR"
                        # クリア済みステージ用のCSSクラスを適用
                        st.markdown('<div class="cleared-stage">', unsafe_allow_html=True)
                        button_clicked = st.button(button_text, key=f"stage_{stage_num}", use_container_width=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                    else:
                        button_text = "▶︎"
                        button_clicked = st.button(button_text, key=f"stage_{stage_num}", use_container_width=True)
                    
                    if button_clicked:
                        st.session_state.current_stage = stage_num
                        st.session_state.target_words = stage_info['words']
                        st.session_state.found_words = []
                        st.session_state.hints_used = []
                        st.session_state.show_hints = {}
                        # 文字をシャッフルして保存
                        stage_letters = stage_info['letters'].copy()
                        random.shuffle(stage_letters)
                        st.session_state.shuffled_letters = stage_letters
                        st.session_state.game_state = 'game'
                        st.rerun()

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
    
    # ヘッダー（3列レイアウト）
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("タイトルに戻る", key="back_to_title_header", use_container_width=True):
            st.session_state.game_state = 'title'
            st.rerun()
    with col2:
        st.markdown(f"""
        <div style="display: flex; justify-content: center; align-items: center; height: 50px;">
            <h2 style="text-align: center; color: #333; margin: 0; line-height: 1.2;">{current_stage_info['name']}</h2>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        # 次のステージボタン（最後のステージでない場合のみ表示）
        if st.session_state.current_stage < len(STAGES):
            if st.button("次のステージへ", key="next_stage_header", use_container_width=True):
                st.session_state.current_stage += 1
                next_stage_info = STAGES[st.session_state.current_stage]
                st.session_state.target_words = next_stage_info['words']
                st.session_state.found_words = []
                st.session_state.hints_used = []
                st.session_state.show_hints = {}
                # 新しいステージの文字をシャッフル
                stage_letters = next_stage_info['letters'].copy()
                random.shuffle(stage_letters)
                st.session_state.shuffled_letters = stage_letters
                st.rerun()
        else:
            # 最後のステージの場合は空のスペース
            st.empty()
    
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
            margin: 200px auto 40px auto;
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
        let targetWords = {json.dumps(st.session_state.target_words)};
        let foundWords = {json.dumps(st.session_state.found_words)};
        let showHints = {json.dumps(st.session_state.show_hints)};

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
                        boxesHtml += '<span style="display: inline-block; width: 26px; height: 26px; border: 1px solid #333; background: white; color: #333; text-align: center; line-height: 26px; margin: 1px; font-size: 14px; font-weight: bold; border-radius: 3px; vertical-align: top;">' + letter + '</span>';
                    }} else if (hasHint && i === 0) {{
                        boxesHtml += '<span style="display: inline-block; width: 26px; height: 26px; border: 1px solid #FF9800; background: #FFF8E1; color: #FF9800; text-align: center; line-height: 26px; margin: 1px; font-size: 14px; font-weight: bold; border-radius: 3px; vertical-align: top;">' + letter + '</span>';
                    }} else {{
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
                        // ステージクリア状態をStreamlitに通知
                        window.parent.postMessage({{
                            type: 'stage_complete',
                            stage: {st.session_state.current_stage},
                            foundWords: foundWords
                        }}, '*');
                    }}, 1000);
                }}
                return true;
            }}
            return false;
        }}
        
        function showHint() {{
            let unfoundWords = targetWords.filter(word => !foundWords.includes(word));
            let availableHints = unfoundWords.filter(word => !showHints.hasOwnProperty(word));
            
            if (availableHints.length > 0) {{
                let randomIndex = Math.floor(Math.random() * availableHints.length);
                let hintWord = availableHints[randomIndex];
                showHints[hintWord] = hintWord[0];
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
                
                button.offsetHeight;
            }}
        }}

        function clearAllSelections() {{
            document.querySelectorAll('.circle-button').forEach(button => {{
                button.classList.remove('selected');
                button.classList.remove('hover');
                button.offsetHeight;
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
                
                if (distance <= 40 && distance < closestDistance) {{
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

        function handleTouchStart(event) {{
            event.preventDefault();
            isDragging = true;
            clearAllSelections();
            
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
                    clearAllSelections();
                }}, isCorrect ? 1000 : 200);
            }}
        }}

        document.addEventListener('mousedown', handleMouseDown);
        document.addEventListener('mousemove', handleMouseMove);
        document.addEventListener('mouseup', handleMouseUp);

        document.addEventListener('touchstart', handleTouchStart, {{passive: false}});
        document.addEventListener('touchmove', handleTouchMove, {{passive: false}});
        document.addEventListener('touchend', handleTouchEnd, {{passive: false}});

        updateSelectedWord();
        updateTargetWordsDisplay();

        document.addEventListener('contextmenu', e => e.preventDefault());
        document.addEventListener('selectstart', e => e.preventDefault());
        </script>
    </body>
    </html>
    """, height=600)

    # ステージクリア状態の確認とボタン表示
    stage_completed = len(st.session_state.found_words) == len(st.session_state.target_words)
    
    if stage_completed:
        # ステージクリア時に cleared_stages に追加
        if st.session_state.current_stage not in st.session_state.cleared_stages:
            st.session_state.cleared_stages.add(st.session_state.current_stage)
        
        st.success("ステージクリア！")
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.session_state.current_stage < len(STAGES):
                if st.button("次のステージへ ", key="next_stage_main", use_container_width=True, type="primary"):
                    st.session_state.current_stage += 1
                    next_stage_info = STAGES[st.session_state.current_stage]
                    st.session_state.target_words = next_stage_info['words']
                    st.session_state.found_words = []
                    st.session_state.hints_used = []
                    st.session_state.show_hints = {}
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
                    st.session_state.current_stage = 1
                    st.session_state.found_words = []
                    st.session_state.hints_used = []
                    st.session_state.show_hints = {}
                    st.session_state.shuffled_letters = []
                    st.rerun()