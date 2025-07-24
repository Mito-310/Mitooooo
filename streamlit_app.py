import streamlit as st
import pandas as pd
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
            problem_text = str(row.iloc[0]).strip()  # 最初の列を問題文として使用
            
            # 問題文から文字を抽出（重複を除去）
            unique_letters = list(set(problem_text.upper().replace(' ', '')))
            
            # 2列目以降から単語を抽出
            words = []
            for col_idx in range(1, len(row)):
                if pd.notna(row.iloc[col_idx]):
                    word = str(row.iloc[col_idx]).strip().upper()
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
if 'current_stage' not in st.session_state:
    st.session_state.current_stage = 1
if 'found_words' not in st.session_state:
    st.session_state.found_words = []
if 'stages' not in st.session_state:
    st.session_state.stages = None

# Excelファイルから問題を読み込み
if st.session_state.stages is None:
    try:
        loaded_stages = load_problems_from_excel('problems.xlsx')
        if loaded_stages:
            st.session_state.stages = loaded_stages
            st.success(f"✅ Excelファイルから{len(loaded_stages)}個のステージを読み込みました")
        else:
            st.session_state.stages = DEFAULT_STAGES
            st.warning("⚠️ Excelファイルの読み込みに失敗しました。デフォルトステージを使用します。")
    except:
        st.session_state.stages = DEFAULT_STAGES
        st.warning("⚠️ problems.xlsxが見つかりません。デフォルトステージを使用します。")

STAGES = st.session_state.stages

# ファイルアップロード機能
st.sidebar.header("📁 問題ファイルの管理")

uploaded_file = st.sidebar.file_uploader(
    "新しい問題ファイルをアップロード", 
    type=['xlsx', 'xls'],
    help="1列目: 問題文、2列目以降: 正答単語のExcelファイルをアップロードしてください"
)

if uploaded_file is not None:
    try:
        # アップロードされたファイルから問題を読み込み
        df = pd.read_excel(uploaded_file)
        
        # データの確認
        st.sidebar.write("📋 アップロードされたファイルの内容:")
        st.sidebar.dataframe(df.head())
        
        if st.sidebar.button("この問題ファイルを使用"):
            new_stages = {}
            for index, row in df.iterrows():
                stage_num = index + 1
                problem_text = str(row.iloc[0]).strip()
                
                # 問題文から文字を抽出
                unique_letters = list(set(problem_text.upper().replace(' ', '')))
                
                # 回答列から単語を抽出
                words = []
                for col_idx in range(1, len(row)):
                    if pd.notna(row.iloc[col_idx]):
                        word = str(row.iloc[col_idx]).strip().upper()
                        if word and word not in words:
                            words.append(word)
                
                new_stages[stage_num] = {
                    'name': f'ステージ {stage_num}',
                    'problem_text': problem_text,
                    'letters': unique_letters,
                    'words': words
                }
            
            st.session_state.stages = new_stages
            st.session_state.current_stage = 1
            st.session_state.found_words = []
            st.sidebar.success(f"🎉 新しい問題ファイルから{len(new_stages)}個のステージを読み込みました！")
            st.rerun()
    
    except Exception as e:
        st.sidebar.error(f"❌ ファイル読み込みエラー: {e}")

# 現在の問題ファイル情報
st.sidebar.write(f"📊 現在のステージ数: {len(STAGES)}")
if st.sidebar.button("🔄 デフォルトステージに戻す"):
    st.session_state.stages = DEFAULT_STAGES
    st.session_state.current_stage = 1
    st.session_state.found_words = []
    st.rerun()

# メインゲーム画面
st.title("🎯 Word Connect")

# 現在のステージ情報を取得
if st.session_state.current_stage in STAGES:
    current_stage_info = STAGES[st.session_state.current_stage]
else:
    st.session_state.current_stage = 1
    current_stage_info = STAGES[1]

st.header(f"🎮 {current_stage_info['name']}")

# 問題文の表示
st.info(f"💡 問題文: {current_stage_info['problem_text']}")

# ステージ選択
st.subheader("📋 ステージ選択")
stage_cols = st.columns(min(5, len(STAGES)))  # 最大5列で表示

for i, stage_num in enumerate(list(STAGES.keys())[:5]):  # 最初の5ステージを表示
    col_idx = i % 5
    with stage_cols[col_idx]:
        stage_info = STAGES[stage_num]
        button_text = f"ステージ {stage_num}\n({len(stage_info['words'])}単語)"
        if st.button(button_text, key=f"stage_{stage_num}"):
            st.session_state.current_stage = stage_num
            st.session_state.found_words = []
            st.rerun()

# 追加のステージがある場合
if len(STAGES) > 5:
    st.write("...")
    selected_stage = st.selectbox(
        "他のステージを選択:",
        options=list(STAGES.keys()),
        index=st.session_state.current_stage - 1,
        format_func=lambda x: f"ステージ {x} ({len(STAGES[x]['words'])}単語)"
    )
    if selected_stage != st.session_state.current_stage:
        st.session_state.current_stage = selected_stage
        st.session_state.found_words = []
        st.rerun()

# リセットボタン
if st.button("🔄 リセット"):
    st.session_state.found_words = []
    st.rerun()

# 進行状況
target_words = current_stage_info['words']
found_words = st.session_state.found_words
progress = len(found_words) / len(target_words) if target_words else 0
st.progress(progress)
st.write(f"📈 進行状況: {len(found_words)} / {len(target_words)} 単語")

# 目標単語表示
st.subheader("🎯 目標単語")
cols = st.columns(3)
for i, word in enumerate(target_words):
    col_idx = i % 3
    with cols[col_idx]:
        status = "✅" if word in found_words else "⬜"
        st.write(f"{status} {word}")

# 見つけた単語表示
if found_words:
    st.success(f"🎉 見つけた単語: {', '.join(found_words)}")

# ゲーム画面
letters = current_stage_info['letters']
num_letters = len(letters)

# 円形ボタンのHTML生成
button_html = ''.join([
    f'''
    <div class="circle-button" 
         data-letter="{letter}"
         data-index="{i}"
         style="left: {150 + 120 * math.cos(2 * math.pi * i / num_letters - math.pi/2) - 25}px;
                top:  {150 + 120 * math.sin(2 * math.pi * i / num_letters - math.pi/2) - 25}px;">
        {letter}
    </div>
    ''' for i, letter in enumerate(letters)
])

# JavaScriptデータ
js_target_words = str(target_words).replace("'", '"')
js_found_words = str(found_words).replace("'", '"')

html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
    body {{
        margin: 0;
        font-family: Arial, sans-serif;
        user-select: none;
        background: #f5f5f5;
    }}
    .circle-container {{
        position: relative;
        width: 300px;
        height: 300px;
        margin: 20px auto;
        border: 2px solid #333;
        border-radius: 50%;
        background: white;
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
    }}
    .circle-button.selected {{
        background: #333;
        color: white;
    }}
    .circle-button:hover {{
        background: #eee;
    }}
    #selected-word {{
        text-align: center;
        font-size: 24px;
        font-weight: bold;
        padding: 20px;
        color: #333;
        min-height: 30px;
    }}
    canvas {{
        position: absolute;
        top: 0;
        left: 0;
        pointer-events: none;
    }}
    .message {{
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background: #4CAF50;
        color: white;
        padding: 20px;
        border-radius: 10px;
        font-size: 18px;
        font-weight: bold;
        z-index: 1000;
        opacity: 0;
        transition: opacity 0.3s ease;
    }}
    .message.show {{
        opacity: 1;
    }}
    .wrong-message {{
        background: #f44336;
    }}
    </style>
</head>
<body>
    <div id="selected-word">文字を繋げて単語を作ってください</div>
    <div id="message" class="message">正解！</div>
    <div id="wrong-message" class="message wrong-message">不正解</div>
    
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

        const selectedWordDiv = document.getElementById('selected-word');
        const messageDiv = document.getElementById('message');
        const wrongMessageDiv = document.getElementById('wrong-message');
        const container = document.getElementById('circle-container');
        const canvas = document.getElementById('lineCanvas');
        const ctx = canvas.getContext('2d');

        function updateSelectedWord() {{
            selectedWordDiv.textContent = selectedLetters.length > 0 ? 
                selectedLetters.join('') : '文字を繋げて単語を作ってください';
        }}

        function checkCorrectWord() {{
            const currentWord = selectedLetters.join('').toUpperCase();
            if (currentWord.length === 0) return false;
            
            if (targetWords.includes(currentWord) && !foundWords.includes(currentWord)) {{
                foundWords.push(currentWord);
                showMessage(true);
                
                // Streamlitに通知
                setTimeout(() => {{
                    window.parent.postMessage({{
                        type: 'streamlit:setComponentValue',
                        value: currentWord
                    }}, '*');
                }}, 500);
                
                return true;
            }} else if (currentWord.length > 0) {{
                showMessage(false);
                return false;
            }}
            return false;
        }}

        function showMessage(isCorrect) {{
            const msgDiv = isCorrect ? messageDiv : wrongMessageDiv;
            msgDiv.classList.add('show');
            setTimeout(() => {{
                msgDiv.classList.remove('show');
            }}, 1500);
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
                for (let i = 1; i < points.length; i++) {{
                    ctx.lineTo(points[i].x, points[i].y);
                }}
                ctx.stroke();
            }}
        }}

        // マウスイベント
        container.addEventListener('mousedown', (e) => {{
            const button = getButtonAtPosition(e.clientX, e.clientY);
            if (button) {{
                isDragging = true;
                resetSelection();
                selectButton(button);
            }}
        }});

        container.addEventListener('mousemove', (e) => {{
            if (isDragging) {{
                const button = getButtonAtPosition(e.clientX, e.clientY);
                if (button && !selectedButtons.includes(button)) {{
                    selectButton(button);
                }}
            }}
        }});

        container.addEventListener('mouseup', () => {{
            if (isDragging) {{
                isDragging = false;
                if (selectedLetters.length > 0) {{
                    const found = checkCorrectWord();
                    setTimeout(resetSelection, found ? 500 : 1000);
                }}
            }}
        }});

        // タッチイベント
        container.addEventListener('touchstart', (e) => {{
            e.preventDefault();
            const touch = e.touches[0];
            const button = getButtonAtPosition(touch.clientX, touch.clientY);
            if (button) {{
                isDragging = true;
                resetSelection();
                selectButton(button);
            }}
        }});

        container.addEventListener('touchmove', (e) => {{
            e.preventDefault();
            if (isDragging) {{
                const touch = e.touches[0];
                const button = getButtonAtPosition(touch.clientX, touch.clientY);
                if (button && !selectedButtons.includes(button)) {{
                    selectButton(button);
                }}
            }}
        }});

        container.addEventListener('touchend', (e) => {{
            e.preventDefault();
            if (isDragging) {{
                isDragging = false;
                if (selectedLetters.length > 0) {{
                    const found = checkCorrectWord();
                    setTimeout(resetSelection, found ? 500 : 1000);
                }}
            }}
        }});

        // 初期化
        updateSelectedWord();
    </script>
</body>
</html>
"""

# HTMLコンポーネントを表示
found_word = components.html(html_content, height=400, scrolling=False)

# 単語が見つかった場合の処理
if found_word and found_word not in st.session_state.found_words:
    st.session_state.found_words.append(found_word)
    st.rerun()

# ステージクリア判定
if len(st.session_state.found_words) == len(target_words):
    st.balloons()
    st.success("🎉 ステージクリア！おめでとうございます！")
    
    # 次のステージがある場合
    next_stage = st.session_state.current_stage + 1
    if next_stage in STAGES:
        if st.button(f"🚀 次のステージ ({next_stage}) へ進む"):
            st.session_state.current_stage = next_stage
            st.session_state.found_words = []
            st.rerun()