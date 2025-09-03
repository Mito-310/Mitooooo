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

/* ステージ選択エリアのスタイル */
.stage-grid {
    display: flex;
    flex-direction: column;
    gap: 20px;
    max-width: 600px;
    margin: 0 auto;
}

.stage-row {
    display: flex;
    justify-content: center;
    gap: 30px;
    flex-wrap: wrap;
}

.stage-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    min-width: 120px;
}

.stage-info {
    text-align: center;
    margin-bottom: 8px;
    color: #555;
    font-weight: 500;
    font-size: 14px;
}

/* 通常のステージボタン */
.stage-button {
    width: 120px;
    height: 50px;
    background-color: #333;
    color: white;
    border: 2px solid #333;
    border-radius: 8px;
    font-weight: 600;
    font-size: 16px;
    cursor: pointer;
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
    justify-content: center;
}

.stage-button:hover {
    background-color: #555;
    border-color: #555;
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
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

if 'temp_found_words' not in st.session_state:
    st.session_state.temp_found_words = []

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
        margin: 3rem 0 2rem 0;
        font-size: 1.8rem;
        font-weight: 600;
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
        <h1 class="game-title">RINGLISH!</h1>
        <div class="game-rules">
            <h3>ゲームルール</h3>
            <p>リング状に配置された文字をなぞって繋げて単語を作るゲームです</p>
            <p>すべての目標単語を見つけるとステージクリア！</p>
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
            st.session_state.temp_found_words = []
            st.session_state.hints_used = []
            st.session_state.show_hints = {}
            # 文字をシャッフルして保存
            stage_letters = STAGES[1]['letters'].copy()
            random.shuffle(stage_letters)
            st.session_state.shuffled_letters = stage_letters
            st.session_state.game_state = 'game'
            st.rerun()
    
    # 区切り線
    st.markdown('<hr style="border: none; height: 2px; background: linear-gradient(90deg, transparent 0%, #ddd 50%, transparent 100%); margin: 3rem 0;">', unsafe_allow_html=True)
    
    # ステージ選択
    st.markdown('<h2 class="stage-selection-title">ステージ選択</h2>', unsafe_allow_html=True)
    
    # ステージ選択を通常のStreamlitボタンで実装
    for i in range(0, len(STAGES), 3):
        cols = st.columns(3)
        for j in range(3):
            stage_num = i + j + 1
            if stage_num <= len(STAGES):
                stage_info = STAGES[stage_num]
                
                with cols[j]:
                    # ステージ情報を表示
                    st.markdown(f'<div style="text-align: center; margin-bottom: 8px; color: #555; font-weight: 500; font-size: 14px;">{stage_info["name"]}</div>', unsafe_allow_html=True)
                    
                    # ボタン
                    button_text = "▶"
                    if st.button(button_text, key=f"stage_{stage_num}", use_container_width=True):
                        st.session_state.current_stage = stage_num
                        st.session_state.target_words = stage_info['words']
                        st.session_state.found_words = []
                        st.session_state.temp_found_words = []
                        st.session_state.hints_used = []
                        st.session_state.show_hints = {}
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
        if i + 3 < len(STAGES):
            st.markdown('<div style="margin: 20px 0;"></div>', unsafe_allow_html=True)

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
            # ステージクリア状態は維持したままタイトルに戻る
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
                st.session_state.temp_found_words = []
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
        word_hints = st.session_state.show_hints.get(word, [])
        boxes_html = ""
        for i, letter in enumerate(word):
            if is_found:
                # 正解済みの単語は全文字表示
                boxes_html += f'<span style="display: inline-block; width: 26px; height: 26px; border: 1px solid #333; background: white; color: #333; text-align: center; line-height: 26px; margin: 1px; font-size: 14px; font-weight: bold; border-radius: 3px; vertical-align: top;">{letter}</span>'
            elif i in word_hints:
                # ヒントがある文字をオレンジで表示
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
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
        body {{
            margin: 0;
            font-family: Arial, sans-serif;
            user-select: none;
            background: #fafafa;
            min-height: 100vh;
            padding-bottom: 20px;
        }}
        
        .game-container {{
            position: relative;
            width: 100%;
            min-height: calc(100vh - 20px);
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
            touch-action: none;
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
        
        .hint-button {{
            position: fixed;
            top: 10px;
            right: 10px;
            z-index: 1002;
            padding: 10px 18px;
            background: #333;
            color: white;
            border: 2px solid #333;
            border-radius: 6px;
            font-weight: bold;
            font-size: 14px;
            cursor: pointer;
            transition: all 0.2s ease;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            -webkit-tap-highlight-color: transparent;
            touch-action: manipulation;
        }}
        
        .hint-button:hover {{
            background: #555;
            border-color: #555;
            transform: translateY(-1px);
            box-shadow: 0 3px 6px rgba(0,0,0,0.2);
        }}
        
        .hint-button:active {{
            transform: translateY(0);
            background: #222;
            border-color: #222;
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
        
        /* モバイル対応 */
        @media (max-width: 768px) {{
            .circle-container {{
                margin-top: 150px;
            }}
            
            .hint-button {{
                padding: 12px 20px;
                font-size: 16px;
                top: 8px;
                right: 8px;
            }}
        }}
        </style>
    </head>
    <body>
        <div class="game-container">
            <div id="selected-word"></div>
            <div id="target-words">{target_display}</div>
            <div id="success-message" class="success-message">正解！</div>
            <div id="complete-message" class="complete-message">ステージクリア！</div>
            
            <button class="hint-button" id="hint-button">ヒント</button>

            <div class="circle-container" id="circle-container">
                <canvas id="lineCanvas" width="320" height="320"></canvas>
                {button_html}
            </div>
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
        const hintButton = document.getElementById('hint-button');

        // ヒントボタンのイベント処理を改善
        function setupHintButton() {{
            // 既存のイベントリスナーを削除
            hintButton.onclick = null;
            
            // タッチイベント用のフラグ
            let touchHandled = false;
            
            // タッチスタート
            hintButton.addEventListener('touchstart', function(e) {{
                e.preventDefault();
                e.stopPropagation();
                touchHandled = true;
                this.style.background = '#222';
                this.style.borderColor = '#222';
                this.style.transform = 'translateY(0)';
            }}, {{passive: false}});
            
            // タッチエンド
            hintButton.addEventListener('touchend', function(e) {{
                e.preventDefault();
                e.stopPropagation();
                if (touchHandled) {{
                    this.style.background = '#333';
                    this.style.borderColor = '#333';
                    this.style.transform = 'translateY(-1px)';
                    showHint();
                    touchHandled = false;
                }}
            }}, {{passive: false}});
            
            // マウスイベント（デスクトップ用）
            hintButton.addEventListener('click', function(e) {{
                if (!touchHandled) {{
                    e.preventDefault();
                    e.stopPropagation();
                    showHint();
                }}
            }});
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
            
            for (let word of sortedWords) {{
                let isFound = foundWords.includes(word);
                let wordHints = showHints[word] || [];
                let boxesHtml = "";
                for (let i = 0; i < word.length; i++) {{
                    let letter = word[i];
                    if (isFound) {{
                        boxesHtml += '<span style="display: inline-block; width: 26px; height: 26px; border: 1px solid #333; background: white; color: #333; text-align: center; line-height: 26px; margin: 1px; font-size: 14px; font-weight: bold; border-radius: 3px; vertical-align: top;">' + letter + '</span>';
                    }} else if (wordHints.includes(i)) {{
                        boxesHtml += '<span style="display: inline-block; width: 26px; height: 26px; border: 1px solid #FF9800; background: #FFF8E1; color: #FF9800; text-align: center; line-height: 26px; margin: 1px; font-size: 14px; font-weight: bold; border-radius: 3px; vertical-align: top;">' + letter + '</span>';
                    }} else {{
                        boxesHtml += '<span style="display: inline-block; width: 26px; height: 26px; border: 1px solid #ddd; background: white; text-align: center; line-height: 26px; margin: 1px; border-radius: 3px; vertical-align: top;"></span>';
                    }}
                }}
                targetBoxesHtml.push('<div style="display: inline-block; margin: 6px; vertical-align: top;">' + boxesHtml + '</div>');
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
        
        function showHint() {{
            let unfoundWords = targetWords.filter(word => !foundWords.includes(word));
            
            if (unfoundWords.length > 0) {{
                // ランダムに単語を選択
                let randomIndex = Math.floor(Math.random() * unfoundWords.length);
                let hintWord = unfoundWords[randomIndex];
                
                // その単語の現在のヒント状況を確認
                let currentHints = showHints[hintWord] || [];
                
                // 最後の文字以外で未解放の文字のインデックスを取得
                let availablePositions = [];
                for (let i = 0; i < hintWord.length - 1; i++) {{
                    if (!currentHints.includes(i)) {{
                        availablePositions.push(i);
                    }}
                }}
                
                if (availablePositions.length > 0) {{
                    // 利用可能な位置からランダムに選択
                    let randomPos = Math.floor(Math.random() * availablePositions.length);
                    let newHintPosition = availablePositions[randomPos];
                    
                    // ヒントを追加
                    if (!showHints[hintWord]) {{
                        showHints[hintWord] = [];
                    }}
                    showHints[hintWord].push(newHintPosition);
                    
                    updateTargetWordsDisplay();
                    
                    // Streamlitにヒント情報を通知
                    window.parent.postMessage({{
                        type: 'hint_used',
                        word: hintWord,
                        position: newHintPosition,
                        hints: showHints
                    }}, '*');
                }}
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

        // 改善されたイベント処理
        function handleInteractionStart(clientX, clientY) {{
            isDragging = true;
            clearAllSelections();
            
            const button = getButtonAtPosition(clientX, clientY);
            if (button) {{
                selectButton(button);
            }}
        }}

        function handleInteractionMove(clientX, clientY) {{
            if (isDragging) {{
                const button = getButtonAtPosition(clientX, clientY);
                if (button) {{
                    selectButton(button);
                }}
            }} else {{
                getButtonAtPosition(clientX, clientY);
            }}
        }}

        function handleInteractionEnd() {{
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

        // マウスイベント
        container.addEventListener('mousedown', function(e) {{
            e.preventDefault();
            handleInteractionStart(e.clientX, e.clientY);
        }});

        document.addEventListener('mousemove', function(e) {{
            e.preventDefault();
            handleInteractionMove(e.clientX, e.clientY);
        }});

        document.addEventListener('mouseup', function(e) {{
            e.preventDefault();
            handleInteractionEnd();
        }});

        // タッチイベント（改善版）
        container.addEventListener('touchstart', function(e) {{
            e.preventDefault();
            const touch = e.touches[0];
            handleInteractionStart(touch.clientX, touch.clientY);
        }}, {{passive: false}});

        document.addEventListener('touchmove', function(e) {{
            e.preventDefault();
            if (isDragging) {{
                const touch = e.touches[0];
                handleInteractionMove(touch.clientX, touch.clientY);
            }}
        }}, {{passive: false}});

        document.addEventListener('touchend', function(e) {{
            e.preventDefault();
            handleInteractionEnd();
        }}, {{passive: false}});

        // 初期化
        setupHintButton();
        updateSelectedWord();
        updateTargetWordsDisplay();

        // コンテキストメニューと選択を無効化
        document.addEventListener('contextmenu', e => e.preventDefault());
        document.addEventListener('selectstart', e => e.preventDefault());
        </script>
    </body>
    </html>
    """, height=600)

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
        if (event.data.type === 'hint_used') {
            // ヒント使用をURLパラメータで通知
            const currentUrl = new URL(window.location);
            currentUrl.searchParams.set('hint_word', event.data.word);
            currentUrl.searchParams.set('hint_position', event.data.position);
            currentUrl.searchParams.set('hint_data', JSON.stringify(event.data.hints));
            window.location.href = currentUrl.toString();
        }
        if (event.data.type === 'stage_complete') {
            // ステージクリア通知（特別な処理は不要）
            console.log('Stage completed:', event.data.stage);
        }
    });
    </script>
    """, height=0)
    
    # ヒント使用のチェック
    if "hint_word" in query_params and "hint_position" in query_params:
        hint_word = query_params["hint_word"]
        hint_position = int(query_params["hint_position"])
        if hint_word not in st.session_state.show_hints:
            st.session_state.show_hints[hint_word] = []
        if hint_position not in st.session_state.show_hints[hint_word]:
            st.session_state.show_hints[hint_word].append(hint_position)
        # クエリパラメータをクリア
        st.query_params.clear()
        st.rerun()
    
    # ステージクリア状態の確認
    stage_completed = len(st.session_state.found_words) == len(st.session_state.target_words)
    
    if stage_completed:
        st.success("ステージクリア！")
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.session_state.current_stage < len(STAGES):
                if st.button("次のステージへ ", key="next_stage_main", use_container_width=True, type="primary"):
                    st.session_state.current_stage += 1
                    next_stage_info = STAGES[st.session_state.current_stage]
                    st.session_state.target_words = next_stage_info['words']
                    st.session_state.found_words = []
                    st.session_state.temp_found_words = []
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
                    # ステージクリア状態は維持したままタイトルに戻る
                    st.rerun()