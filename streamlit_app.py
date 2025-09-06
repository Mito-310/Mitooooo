import streamlit as st
import random
import math
import json
import streamlit.components.v1 as components

# ページ設定
st.set_page_config(
    page_title="RINGLISH",
    layout="centered",
    initial_sidebar_state="auto"
)

# カスタムCSS - スマホファースト
st.markdown("""
<style>
/* 全体の基本設定 - スマホファースト */
.main .block-container {
    max-width: 100vw;
    padding: 0.3rem;
    margin: 0;
}

/* タイトル画面のボタンスタイル */
.stButton > button {
    background-color: #333;
    color: white;
    border: 1px solid #333;
    border-radius: 4px;
    font-weight: 500;
    transition: all 0.2s ease;
    height: 32px;
    font-size: 13px;
}

.stButton > button:hover {
    background-color: #555;
    border-color: #555;
}

/* SUCCESS/エラーメッセージの調整 */
.stSuccess {
    background-color: #E8F5E8;
    border-left: 3px solid #4CAF50;
    padding: 6px 8px;
    margin: 6px 0;
    font-size: 13px;
}

/* ステージ選択エリアのスタイル */
.stage-info {
    text-align: center;
    margin-bottom: 4px;
    color: #555;
    font-weight: 500;
    font-size: 11px;
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

def create_target_words_display(words, found_words, max_width_chars=25):
    """目標単語を複数行で表示するHTMLを生成 - スマホ用に小さく"""
    sorted_words = sorted(words, key=lambda x: (len(x), x))
    
    # 単語を配置する
    lines = []
    current_line = []
    current_width = 0
    
    for word in sorted_words:
        word_width = len(word) + 1  # +1はマージン分
        
        # 新しい行が必要かチェック
        if current_width + word_width > max_width_chars and current_line:
            lines.append(current_line)
            current_line = [word]
            current_width = word_width
        else:
            current_line.append(word)
            current_width += word_width
    
    if current_line:
        lines.append(current_line)
    
    # HTMLを生成 - スマホ用に小さく
    html_lines = []
    for line_words in lines:
        line_html = []
        for word in line_words:
            is_found = word in found_words
            boxes_html = ""
            for letter in word:
                if is_found:
                    boxes_html += f'<span style="display: inline-block; width: 16px; height: 16px; border: 1px solid #333; background: white; color: #333; text-align: center; line-height: 16px; margin: 0.5px; font-size: 10px; font-weight: bold; border-radius: 2px; vertical-align: top;">{letter}</span>'
                else:
                    boxes_html += f'<span style="display: inline-block; width: 16px; height: 16px; border: 1px solid #ddd; background: white; text-align: center; line-height: 16px; margin: 0.5px; border-radius: 2px; vertical-align: top;"></span>'
            line_html.append(f'<div style="display: inline-block; margin: 2px; vertical-align: top;">{boxes_html}</div>')
        html_lines.append('<div style="text-align: center; margin-bottom: 3px;">' + ''.join(line_html) + '</div>')
    
    return ''.join(html_lines)

# タイトル画面
if st.session_state.game_state == 'title':
    st.markdown("""
    <style>
    .title-section {
        text-align: center;
        padding: 0.5rem 0.3rem;
        margin-bottom: 0.5rem;
    }
    .game-title {
        font-size: 1.8rem;
        font-weight: 700;
        color: #333;
        margin-bottom: 0.5rem;
        letter-spacing: 1px;
    }
    .game-rules {
        max-width: 95vw;
        margin: 0 auto;
        padding: 0.8rem;
        background: #f8f9fa;
        border-radius: 6px;
        text-align: left;
        margin-bottom: 0.8rem;
    }
    .game-rules p {
        color: #555;
        line-height: 1.4;
        margin-bottom: 0.4rem;
        font-size: 13px;
    }
    .stage-selection-title {
        text-align: center;
        color: #333;
        margin: 1.5rem 0 1rem 0;
        font-size: 1.2rem;
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
            st.markdown(f'<div style="text-align: center; margin: 10px 0;"><img src="data:image/png;base64,{img_str}" width="80" style="max-width: 100%; border-radius: 4px;"></div>', unsafe_allow_html=True)
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
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("START", key="start_button", use_container_width=True):
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
    st.markdown('<hr style="border: none; height: 1px; background: #ddd; margin: 1.5rem 0;">', unsafe_allow_html=True)
    
    # ステージ選択
    st.markdown('<h2 class="stage-selection-title">ステージ選択</h2>', unsafe_allow_html=True)
    
    # ステージ選択を通常のStreamlitボタンで実装
    for i in range(0, len(STAGES), 4):
        cols = st.columns(4)
        for j in range(4):
            stage_num = i + j + 1
            if stage_num <= len(STAGES):
                stage_info = STAGES[stage_num]
                
                with cols[j]:
                    # ステージ情報を表示
                    st.markdown(f'<div style="text-align: center; margin-bottom: 4px; color: #555; font-weight: 500; font-size: 11px;">{stage_info["name"]}</div>', unsafe_allow_html=True)
                    
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
        if i + 4 < len(STAGES):
            st.markdown('<div style="margin: 8px 0;"></div>', unsafe_allow_html=True)

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
    
    # ヘッダー（3列レイアウト） - スマホ用に小さく
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("戻る", key="back_to_title_header", use_container_width=True):
            st.session_state.game_state = 'title'
            st.rerun()
    with col2:
        st.markdown(f"""
        <div style="display: flex; justify-content: center; align-items: center; height: 32px;">
            <h3 style="text-align: center; color: #333; margin: 0; line-height: 1.2; font-size: 16px;">{current_stage_info['name']}</h3>
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
    
    # JavaScriptから送信されたアクションをチェック
    query_params = st.query_params
    if "correct_word" in query_params:
        correct_word = query_params["correct_word"]
        if correct_word not in st.session_state.found_words:
            st.session_state.found_words.append(correct_word)
        # クエリパラメータをクリア
        st.query_params.clear()
        st.rerun()
    
    if "action" in query_params:
        action = query_params["action"]
        if action == "back_to_title":
            st.session_state.game_state = 'title'
            st.query_params.clear()
            st.rerun()
        elif action == "next_stage" and st.session_state.current_stage < len(STAGES):
            st.session_state.current_stage += 1
            next_stage_info = STAGES[st.session_state.current_stage]
            st.session_state.target_words = next_stage_info['words']
            st.session_state.found_words = []
            st.session_state.temp_found_words = []
            # 新しいステージの文字をシャッフル
            stage_letters = next_stage_info['letters'].copy()
            random.shuffle(stage_letters)
            st.session_state.shuffled_letters = stage_letters
            st.query_params.clear()
            st.rerun()
    
    # 目標単語の表示（複数行対応版を使用）
    target_display = create_target_words_display(st.session_state.target_words, st.session_state.found_words)
    
    # 円形ボタンのHTML生成 - 完全に中央に配置、均等な余白
    # コンテナサイズ: 220px, 中心: 110px
    # 外側円: 直径180px, 半径90px
    # ボタン: 直径30px, 半径15px  
    # ボタン配置半径: 90px - 15px - 10px = 65px (10pxの余白)
    button_html = ''.join([
        f'''
        <div class="circle-button" id="button_{i}"
                data-letter="{letter}"
                data-index="{i}"
                style="left: {110 + 65 * math.cos(2 * math.pi * i / num_letters - math.pi/2) - 15}px;
                       top:  {110 + 65 * math.sin(2 * math.pi * i / num_letters - math.pi/2) - 15}px;">
            {letter}
        </div>
        ''' for i, letter in enumerate(letters)
    ])

    # 完全に分離したHTMLコンテンツ - スマホファースト
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
            height: 100vh;
            position: relative;
            max-width: 100vw;
        }
        
        .circle-container {
            position: relative;
            width: 220px;
            height: 220px;
            margin: 80px auto 20px auto;
        }
        
        .ring-background {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 180px;
            height: 180px;
            border: 1px solid #333;
            border-radius: 50%;
            z-index: 1;
            background: transparent;
        }
        
        .circle-button {
            position: absolute;
            width: 30px;
            height: 30px;
            border-radius: 50%;
            background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
            color: #333;
            font-size: 14px;
            font-weight: bold;
            border: 1.5px solid #333;
            cursor: pointer;
            display: flex;
            justify-content: center;
            align-items: center;
            transition: all 0.15s ease;
            touch-action: none;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            z-index: 10;
        }
        
        .circle-button.selected {
            background: linear-gradient(135deg, #2c2c2c 0%, #1a1a1a 100%) !important;
            color: white !important;
            transform: scale(1.1);
            box-shadow: 0 2px 6px rgba(0,0,0,0.25);
            border: 1.5px solid #1a1a1a;
            transition: all 0.1s ease;
            z-index: 10;
        }
        
        .circle-button:not(.selected):hover {
            background: linear-gradient(135deg, #f0f0f0 0%, #e9ecef 100%) !important;
            transform: scale(1.05);
        }
        
        .circle-button.hover {
            background: linear-gradient(135deg, #f0f0f0 0%, #e9ecef 100%) !important;
            transform: scale(1.05);
        }
        
        #selected-word {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            text-align: center;
            font-size: 16px;
            font-weight: bold;
            padding: 6px;
            letter-spacing: 1px;
            min-height: 20px;
            color: #333;
            background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
            z-index: 999;
            border-bottom: 1px solid #e9ecef;
        }
        
        #target-words {
            position: fixed;
            top: 32px;
            left: 0;
            width: 100%;
            text-align: center;
            font-size: 11px;
            padding: 6px;
            color: #666;
            background: #f9f9f9;
            z-index: 998;
            border-bottom: 1px solid #ddd;
            max-height: 70px;
            overflow-y: auto;
        }
        
        .success-message {
            position: fixed;
            top: 40%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
            color: white;
            padding: 12px 20px;
            border-radius: 6px;
            font-size: 14px;
            font-weight: bold;
            z-index: 1000;
            opacity: 0;
            transition: all 0.3s ease;
        }
        .success-message.show {
            opacity: 1;
            transform: translate(-50%, -50%) scale(1.05);
        }
        .complete-message {
            position: fixed;
            top: 40%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: linear-gradient(135deg, #2196F3 0%, #1976D2 100%);
            color: white;
            padding: 16px 24px;
            border-radius: 8px;
            font-size: 16px;
            font-weight: bold;
            z-index: 1001;
            opacity: 0;
            transition: all 0.3s ease;
        }
        .complete-message.show {
            opacity: 1;
            transform: translate(-50%, -50%) scale(1.05);
        }
        canvas {
            position: absolute;
            top: 0;
            left: 0;
            z-index: 1;
            pointer-events: none;
        }
        </style>
    </head>
    <body>
        <div id="selected-word"></div>
        <div id="target-words">TARGET_WORDS_PLACEHOLDER</div>
        <div id="success-message" class="success-message">正解！</div>
        <div id="complete-message" class="complete-message">ステージクリア！</div>

        <div class="circle-container" id="circle-container">
            <div class="ring-background"></div>
            <canvas id="lineCanvas" width="220" height="220"></canvas>
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
            // この関数はPythonで生成されたHTMLを使用するため、JavaScriptでの更新は不要
            // ただし、必要に応じて動的更新のためのコードをここに配置できます
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
                
                if (distance <= 20 && distance < closestDistance) {
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
                ctx.arc(point.x, point.y, 1.5, 0, 2 * Math.PI);
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

    components.html(html_content, height=320)

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
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
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
                    # スクロール位置リセット用のJavaScriptを追加
                    st.markdown('<script>setTimeout(() => window.scrollTo(0, 0), 100);</script>', unsafe_allow_html=True)
                    # ステージクリア状態は維持したままタイトルに戻る
                    st.rerun()