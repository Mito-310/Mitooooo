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

# カスタムCSS（スマホ最適化）
st.markdown("""
<style>
/* 全体のレスポンシブ調整 */
.main .block-container {
    padding: 1rem !important;
    max-width: 100% !important;
}

/* タイトル画面のボタンスタイル */
.stButton > button {
    background-color: #333;
    color: white;
    border: 2px solid #333;
    border-radius: 8px;
    font-weight: 600;
    transition: all 0.3s ease;
    height: 45px;
    width: 100%;
}

.stButton > button:hover {
    background-color: #555;
    border-color: #555;
    transform: translateY(-1px);
    box-shadow: 0 3px 6px rgba(0,0,0,0.2);
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
    font-size: 14px;
}

.stWarning {
    background-color: #FFF8E1;
    border-left: 4px solid #FF9800;
}

.stError {
    background-color: #FFEBEE;
    border-left: 4px solid #F44336;
}

/* スマホ用のグリッドスタイル */
.stage-grid {
    display: flex;
    flex-direction: column;
    gap: 15px;
    max-width: 100%;
    margin: 0 auto;
    padding: 0 10px;
}

.stage-row {
    display: flex;
    justify-content: space-around;
    gap: 10px;
    flex-wrap: wrap;
}

.stage-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    min-width: 90px;
    flex: 1;
}

.stage-info {
    text-align: center;
    margin-bottom: 6px;
    color: #555;
    font-weight: 500;
    font-size: 12px;
}

/* ステージボタンをスマホサイズに調整 */
.stage-button {
    width: 90px;
    height: 40px;
    background-color: #333;
    color: white;
    border: 2px solid #333;
    border-radius: 6px;
    font-weight: 600;
    font-size: 14px;
    cursor: pointer;
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
    justify-content: center;
}

.stage-button:hover {
    background-color: #555;
    border-color: #555;
    transform: translateY(-1px);
    box-shadow: 0 3px 6px rgba(0,0,0,0.2);
}

/* スマホ用の列調整 */
@media (max-width: 768px) {
    .stColumns {
        gap: 0.5rem !important;
    }
    
    .stButton > button {
        font-size: 14px;
        height: 40px;
    }
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
    st.markdown("""
    <style>
    .title-section {
        text-align: center;
        padding: 1rem 0.5rem;
        margin-bottom: 1rem;
    }
    .game-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #333;
        margin-bottom: 0.8rem;
        letter-spacing: 1px;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.1);
    }
    .game-subtitle {
        font-size: 1.1rem;
        color: #555;
        margin-bottom: 1rem;
        font-weight: 400;
    }
    .game-rules {
        max-width: 100%;
        margin: 0 auto;
        padding: 1.2rem;
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 10px;
        text-align: left;
        margin-bottom: 1rem;
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
        font-size: 14px;
    }
    .stage-selection-title {
        text-align: center;
        color: #333;
        margin: 2rem 0 1.5rem 0;
        font-size: 1.4rem;
        font-weight: 600;
    }
    
    @media (max-width: 768px) {
        .game-title {
            font-size: 1.8rem;
        }
        .game-subtitle {
            font-size: 1rem;
        }
        .stage-selection-title {
            font-size: 1.2rem;
            margin: 1.5rem 0 1rem 0;
        }
        .game-rules {
            padding: 1rem;
        }
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
            st.markdown(f'<div style="text-align: center; margin: 15px 0;"><img src="data:image/png;base64,{img_str}" width="150" style="max-width: 80%; border-radius: 6px; box-shadow: 0 3px 6px rgba(0,0,0,0.1);"></div>', unsafe_allow_html=True)
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

    
    # STARTボタン
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
    st.markdown('<hr style="border: none; height: 1px; background: linear-gradient(90deg, transparent 0%, #ddd 50%, transparent 100%); margin: 2rem 0;">', unsafe_allow_html=True)
    
    # ステージ選択
    st.markdown('<h2 class="stage-selection-title">ステージ選択</h2>', unsafe_allow_html=True)
    
    # ステージ選択をスマホ最適化で実装（2列表示）
    for i in range(0, len(STAGES), 2):
        cols = st.columns(2)
        for j in range(2):
            stage_num = i + j + 1
            if stage_num <= len(STAGES):
                stage_info = STAGES[stage_num]
                
                with cols[j]:
                    # ステージ情報を表示
                    st.markdown(f'<div style="text-align: center; margin-bottom: 6px; color: #555; font-weight: 500; font-size: 12px;">{stage_info["name"]}</div>', unsafe_allow_html=True)
                    
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
            st.markdown('<div style="margin: 15px 0;"></div>', unsafe_allow_html=True)

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
    
    # ヘッダー（3列レイアウト、スマホ最適化）
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("戻る", key="back_to_title_header", use_container_width=True):
            st.session_state.game_state = 'title'
            # ステージクリア状態は維持したままタイトルに戻る
            st.rerun()
    with col2:
        st.markdown(f"""
        <div style="display: flex; justify-content: center; align-items: center; height: 40px;">
            <h2 style="text-align: center; color: #333; margin: 0; line-height: 1.2; font-size: 1.2rem;">{current_stage_info['name']}</h2>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        # 次のステージボタン（常に表示、最後のステージでは無効化）
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
            # 最後のステージの場合は無効化されたボタンを表示
            st.button("次へ", key="next_stage_disabled", use_container_width=True, disabled=True)
    
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
                boxes_html += f'<span style="display: inline-block; width: 22px; height: 22px; border: 1px solid #333; background: white; color: #333; text-align: center; line-height: 22px; margin: 1px; font-size: 12px; font-weight: bold; border-radius: 3px; vertical-align: top;">{letter}</span>'
            else:
                # 通常の空白枠
                boxes_html += f'<span style="display: inline-block; width: 22px; height: 22px; border: 1px solid #ddd; background: white; text-align: center; line-height: 22px; margin: 1px; border-radius: 3px; vertical-align: top;"></span>'
        target_boxes_html.append(f'<div style="display: inline-block; margin: 4px; vertical-align: top;">{boxes_html}</div>')
    
    target_display = ''.join(target_boxes_html)
    
    # 円形ボタンのHTML生成（スマホサイズに調整）
    button_html = ''.join([
        f'''
        <div class="circle-button" id="button_{i}"
                data-letter="{letter}"
                data-index="{i}"
                style="left: {130 + 90 * math.cos(2 * math.pi * i / num_letters - math.pi/2) - 20}px;
                       top:  {130 + 90 * math.sin(2 * math.pi * i / num_letters - math.pi/2) - 20}px;">
            {letter}
        </div>
        ''' for i, letter in enumerate(letters)
    ])

    # 完全に分離したHTMLコンテンツ（スマホ最適化）
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
        <style>
        body {
            margin: 0;
            font-family: Arial, sans-serif;
            user-select: none;
            touch-action: none;
            overflow-x: hidden;
            background: #fafafa;
            min-height: 100vh;
            position: relative;
        }
        
        .circle-container {
            position: relative;
            width: 260px;
            height: 260px;
            margin: 80px auto 30px auto;
            border: 2px solid #ddd;
            border-radius: 50%;
            background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        
        .circle-button {
            position: absolute;
            width: 40px;
            height: 40px;
            border-radius: 50%;
            background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
            color: #333;
            font-size: 16px;
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
        }
        
        .circle-button.selected {
            background: linear-gradient(135deg, #2c2c2c 0%, #1a1a1a 100%) !important;
            color: white !important;
            transform: scale(1.15);
            box-shadow: 0 4px 8px rgba(0,0,0,0.3);
            border: 2px solid #1a1a1a;
            transition: all 0.1s ease;
            z-index: 10;
        }
        
        .circle-button:not(.selected):hover {
            background: linear-gradient(135deg, #f0f0f0 0%, #e9ecef 100%) !important;
            transform: scale(1.05);
            box-shadow: 0 3px 6px rgba(0,0,0,0.15);
        }
        
        .circle-button.hover {
            background: linear-gradient(135deg, #f0f0f0 0%, #e9ecef 100%) !important;
            transform: scale(1.05);
            box-shadow: 0 3px 6px rgba(0,0,0,0.15);
        }
        
        #selected-word {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            text-align: center;
            font-size: 20px;
            font-weight: bold;
            padding: 10px;
            letter-spacing: 3px;
            min-height: 30px;
            color: #333;
            background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
            z-index: 999;
            border-bottom: 2px solid #e9ecef;
        }
        
        #target-words {
            position: fixed;
            top: 50px;
            left: 0;
            width: 100%;
            text-align: center;
            font-size: 14px;
            padding: 12px 8px;
            color: #666;
            background: #f9f9f9;
            z-index: 998;
            border-bottom: 1px solid #ddd;
        }
        
        .success-message {
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
            color: white;
            padding: 15px 25px;
            border-radius: 6px;
            font-size: 16px;
            font-weight: bold;
            z-index: 1000;
            opacity: 0;
            transition: all 0.3s ease;
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
            background: linear-gradient(135deg, #2196F3 0%, #1976D2 100%);
            color: white;
            padding: 20px 30px;
            border-radius: 8px;
            font-size: 18px;
            font-weight: bold;
            z-index: 1001;
            opacity: 0;
            transition: all 0.3s ease;
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
            pointer-events: none;
        }
        
        /* スマホ専用の調整 */
        @media (max-width: 480px) {
            .circle-container {
                width: 240px;
                height: 240px;
                margin: 60px auto 25px auto;
            }
            
            .circle-button {
                width: 35px;
                height: 35px;
                font-size: 14px;
            }
            
            #selected-word {
                font-size: 18px;
                padding: 8px;
                letter-spacing: 2px;
            }
            
            #target-words {
                font-size: 12px;
                padding: 10px 6px;
                top: 46px;
            }
            
            .success-message, .complete-message {
                font-size: 14px;
                padding: 12px 20px;
            }
        }
        </style>
    </head>
    <body>
        <div id="selected-word"></div>
        <div id="target-words">TARGET_WORDS_PLACEHOLDER</div>
        <div id="success-message" class="success-message">正解！</div>
        <div id="complete-message" class="complete-message">ステージクリア！</div>

        <div class="circle-container" id="circle-container">
            <canvas id="lineCanvas" width="260" height="260"></canvas>
            BUTTON_HTML_PLACEHOLDER
        </div>

        <script>
        let isDragging = false;
        let selectedLetters = [];
        let selectedButtons = [];
        let points = [];
        let targetWords = TARGET_WORDS_JSON;
        let foundWords = FOUND_WORDS_JSON;

        const selectedWordDiv = document.getElementById('selected-word');
        const targetWordsDiv = document.getElementById('target-words');
        const successMessageDiv = document.getElementById('success-message');
        const completeMessageDiv = document.getElementById('complete-message');
        const container = document.getElementById('circle-container');
        const canvas = document.getElementById('lineCanvas');
        const ctx = canvas.getContext('2d');

        function createAudioContext() {
            try {
                return new (window.AudioContext || window.webkitAudioContext)();
            } catch (e) {
                console.log('Web Audio API not supported');
                return null;
            }
        }

        const audioCtx = createAudioContext();

        function playSelectSound() {
            if (!audioCtx) return;
            const oscillator = audioCtx.createOscillator();
            const gainNode = audioCtx.createGain();
            oscillator.connect(gainNode);
            gainNode.connect(audioCtx.destination);
            oscillator.frequency.value = 800;
            oscillator.type = 'sine';
            gainNode.gain.setValueAtTime(0.3, audioCtx.currentTime);
            gainNode.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.1);
            oscillator.start(audioCtx.currentTime);
            oscillator.stop(audioCtx.currentTime + 0.1);
        }

        function playCorrectSound() {
            if (!audioCtx) return;
            const frequencies = [523, 659, 784, 1047];
            frequencies.forEach((freq, index) => {
                const oscillator = audioCtx.createOscillator();
                const gainNode = audioCtx.createGain();
                oscillator.connect(gainNode);
                gainNode.connect(audioCtx.destination);
                oscillator.frequency.value = freq;
                oscillator.type = 'sine';
                const startTime = audioCtx.currentTime + index * 0.1;
                gainNode.gain.setValueAtTime(0.2, startTime);
                gainNode.gain.exponentialRampToValueAtTime(0.01, startTime + 0.3);
                oscillator.start(startTime);
                oscillator.stop(startTime + 0.3);
            });
        }

        function playCompleteSound() {
            if (!audioCtx) return;
            const melody = [523, 659, 784, 1047, 1319];
            melody.forEach((freq, index) => {
                const oscillator = audioCtx.createOscillator();
                const gainNode = audioCtx.createGain();
                oscillator.connect(gainNode);
                gainNode.connect(audioCtx.destination);
                oscillator.frequency.value = freq;
                oscillator.type = 'triangle';
                const startTime = audioCtx.currentTime + index * 0.15;
                gainNode.gain.setValueAtTime(0.3, startTime);
                gainNode.gain.exponentialRampToValueAtTime(0.01, startTime + 0.4);
                oscillator.start(startTime);
                oscillator.stop(startTime + 0.4);
            });
        }

        function playWrongSound() {
            if (!audioCtx) return;
            const oscillator = audioCtx.createOscillator();
            const gainNode = audioCtx.createGain();
            oscillator.connect(gainNode);
            gainNode.connect(audioCtx.destination);
            oscillator.frequency.value = 200;
            oscillator.type = 'sawtooth';
            gainNode.gain.setValueAtTime(0.2, audioCtx.currentTime);
            gainNode.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.3);
            oscillator.start(audioCtx.currentTime);
            oscillator.stop(audioCtx.currentTime + 0.3);
        }

        function updateSelectedWord() {
            selectedWordDiv.textContent = selectedLetters.join('');
        }

        function updateTargetWordsDisplay() {
            let targetBoxesHtml = [];
            let sortedWords = targetWords.slice().sort((a, b) => {
                if (a.length !== b.length) {
                    return a.length - b.length;
                }
                return a.localeCompare(b);
            });
            
            for (let word of sortedWords) {
                let isFound = foundWords.includes(word);
                let boxesHtml = "";
                for (let i = 0; i < word.length; i++) {
                    let letter = word[i];
                    if (isFound) {
                        boxesHtml += '<span style="display: inline-block; width: 22px; height: 22px; border: 1px solid #333; background: white; color: #333; text-align: center; line-height: 22px; margin: 1px; font-size: 12px; font-weight: bold; border-radius: 3px; vertical-align: top;">' + letter + '</span>';
                    } else {
                        boxesHtml += '<span style="display: inline-block; width: 22px; height: 22px; border: 1px solid #ddd; background: white; text-align: center; line-height: 22px; margin: 1px; border-radius: 3px; vertical-align: top;"></span>';
                    }
                }
                targetBoxesHtml.push('<div style="display: inline-block; margin: 4px; vertical-align: top;">' + boxesHtml + '</div>');
            }
            
            targetWordsDiv.innerHTML = targetBoxesHtml.join('');
        }

        function notifyCorrectWord(word) {
            window.parent.postMessage({
                type: 'correct_word',
                word: word
            }, '*');
        }

        function checkCorrectWord() {
            const currentWord = selectedLetters.join('');
            if (currentWord && targetWords.includes(currentWord) && !foundWords.includes(currentWord)) {
                foundWords.push(currentWord);
                updateTargetWordsDisplay();
                showSuccessMessage();
                playCorrectSound();
                
                notifyCorrectWord(currentWord);
                
                if (foundWords.length === targetWords.length) {
                    setTimeout(() => {
                        showCompleteMessage();
                        playCompleteSound();
                        window.parent.postMessage({
                            type: 'stage_complete',
                            stage: CURRENT_STAGE_NUM
                        }, '*');
                    }, 1000);
                }
                return true;
            } else if (currentWord && currentWord.length >= 3) {
                playWrongSound();
            }
            return false;
        }

        function showSuccessMessage() {
            successMessageDiv.classList.add('show');
            setTimeout(() => {
                successMessageDiv.classList.remove('show');
            }, 1500);
        }

        function showCompleteMessage() {
            completeMessageDiv.classList.add('show');
            setTimeout(() => {
                completeMessageDiv.classList.remove('show');
            }, 2500);
        }

        function getButtonCenterPosition(button) {
            const rect = button.getBoundingClientRect();
            const containerRect = container.getBoundingClientRect();
            return {
                x: rect.left - containerRect.left + rect.width / 2,
                y: rect.top - containerRect.top + rect.height / 2
            };
        }

        function selectButton(button) {
            if (!selectedButtons.includes(button)) {
                if (audioCtx && audioCtx.state === 'suspended') {
                    audioCtx.resume();
                }
                
                button.classList.add('selected');
                button.classList.remove('hover');
                
                selectedLetters.push(button.dataset.letter);
                selectedButtons.push(button);
                points.push(getButtonCenterPosition(button));
                updateSelectedWord();
                drawLine();
                playSelectSound();
                
                button.offsetHeight;
            }
        }

        function clearAllSelections() {
            document.querySelectorAll('.circle-button').forEach(button => {
                button.classList.remove('selected');
                button.classList.remove('hover');
                button.offsetHeight;
            });
            selectedLetters = [];
            selectedButtons = [];
            points = [];
            updateSelectedWord();
            drawLine();
        }

        function getButtonAtPosition(clientX, clientY) {
            const buttons = document.querySelectorAll('.circle-button');
            let closestButton = null;
            let closestDistance = Infinity;
            
            buttons.forEach(button => {
                if (!button.classList.contains('selected')) {
                    button.classList.remove('hover');
                }
            });
            
            for (let button of buttons) {
                const rect = button.getBoundingClientRect();
                const buttonCenterX = rect.left + rect.width / 2;
                const buttonCenterY = rect.top + rect.height / 2;
                
                const distance = Math.sqrt(
                    Math.pow(clientX - buttonCenterX, 2) + 
                    Math.pow(clientY - buttonCenterY, 2)
                );
                
                if (distance <= 30 && distance < closestDistance) {
                    closestDistance = distance;
                    closestButton = button;
                }
            }
            
            if (closestButton && !closestButton.classList.contains('selected')) {
                closestButton.classList.add('hover');
            }
            
            return closestButton;
        }

        function drawLine() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            if (points.length < 2) return;

            ctx.beginPath();
            ctx.moveTo(points[0].x, points[0].y);
            for (let i = 1; i < points.length; i++) {
                ctx.lineTo(points[i].x, points[i].y);
            }
            ctx.strokeStyle = '#333';
            ctx.lineWidth = 2;
            ctx.stroke();

            points.forEach(point => {
                ctx.beginPath();
                ctx.arc(point.x, point.y, 2, 0, 2 * Math.PI);
                ctx.fillStyle = '#333';
                ctx.fill();
            });
        }

        function handleMouseDown(event) {
            event.preventDefault();
            isDragging = true;
            clearAllSelections();
            
            const button = getButtonAtPosition(event.clientX, event.clientY);
            if (button) {
                selectButton(button);
            }
        }

        function handleMouseMove(event) {
            event.preventDefault();
            
            if (isDragging) {
                const button = getButtonAtPosition(event.clientX, event.clientY);
                if (button) {
                    selectButton(button);
                }
            } else {
                getButtonAtPosition(event.clientX, event.clientY);
            }
        }

        function handleMouseUp(event) {
            event.preventDefault();
            if (isDragging) {
                isDragging = false;
                const isCorrect = checkCorrectWord();
                
                setTimeout(() => {
                    clearAllSelections();
                }, isCorrect ? 1000 : 200);
            }
            document.querySelectorAll('.circle-button').forEach(button => {
                button.classList.remove('hover');
            });
        }

        function handleTouchStart(event) {
            event.preventDefault();
            isDragging = true;
            clearAllSelections();
            
            const touch = event.touches[0];
            const button = getButtonAtPosition(touch.clientX, touch.clientY);
            if (button) {
                selectButton(button);
            }
        }

        function handleTouchMove(event) {
            event.preventDefault();
            if (!isDragging) return;
            
            const touch = event.touches[0];
            const button = getButtonAtPosition(touch.clientX, touch.clientY);
            if (button) {
                selectButton(button);
            }
        }

        function handleTouchEnd(event) {
            event.preventDefault();
            if (isDragging) {
                isDragging = false;
                const isCorrect = checkCorrectWord();
                setTimeout(() => {
                    clearAllSelections();
                }, isCorrect ? 1000 : 200);
            }
        }

        document.addEventListener('mousedown', handleMouseDown);
        document.addEventListener('mousemove', handleMouseMove);
        document.addEventListener('mouseup', handleMouseUp);

        document.addEventListener('touchstart', handleTouchStart, {passive: false});
        document.addEventListener('touchmove', handleTouchMove, {passive: false});
        document.addEventListener('touchend', handleTouchEnd, {passive: false});

        updateSelectedWord();
        updateTargetWordsDisplay();
        
        // 初期ボタン配置
        repositionButtons();

        document.addEventListener('contextmenu', e => e.preventDefault());
        document.addEventListener('selectstart', e => e.preventDefault());
        </script>
    </body>
    </html>
    """

    # プレースホルダーを実際の値で置換
    html_content = html_content.replace('TARGET_WORDS_PLACEHOLDER', target_display)
    html_content = html_content.replace('BUTTON_HTML_PLACEHOLDER', button_html)
    html_content = html_content.replace('TARGET_WORDS_JSON', json.dumps(st.session_state.target_words))
    html_content = html_content.replace('FOUND_WORDS_JSON', json.dumps(st.session_state.found_words))
    html_content = html_content.replace('CURRENT_STAGE_NUM', str(st.session_state.current_stage))

    components.html(html_content, height=600)

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
        if st.session_state.current_stage < len(STAGES):
            if st.button("次のステージへ ", key="next_stage_main", use_container_width=True, type="primary"):
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
                # ステージクリア状態は維持したままタイトルに戻る
                st.rerun()