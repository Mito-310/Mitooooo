import streamlit as st
import random
import math
import json
import streamlit.components.v1 as components
import time

# ページ設定
st.set_page_config(
    page_title="RINGLISH",
    layout="centered",
    initial_sidebar_state="auto"
)

# カスタムCSS - スマホファースト
st.markdown("""
<style>
.main .block-container {
    max-width: 100vw;
    padding: 0.3rem;
    margin: 0;
}

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

.stSuccess {
    background-color: #E8F5E8;
    border-left: 3px solid #4CAF50;
    padding: 6px 8px;
    margin: 6px 0;
    font-size: 13px;
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
if 'last_update_time' not in st.session_state:
    st.session_state.last_update_time = time.time()
if 'game_component_key' not in st.session_state:
    st.session_state.game_component_key = 0

STAGES = DEFAULT_STAGES

def create_target_words_display(words, found_words):
    """目標単語を表示するHTMLを生成"""
    sorted_words = sorted(words, key=lambda x: (len(x), x))
    html_parts = []
    
    for word in sorted_words:
        is_found = word in found_words
        boxes = ""
        for letter in word:
            if is_found:
                boxes += f'<span style="display:inline-block;width:14px;height:14px;border:1px solid #333;background:white;color:#333;text-align:center;line-height:14px;margin:0.5px;font-size:9px;font-weight:bold;">{letter}</span>'
            else:
                boxes += '<span style="display:inline-block;width:14px;height:14px;border:1px solid #ddd;background:white;margin:0.5px;"></span>'
        html_parts.append(f'<div style="display:inline-block;margin:1px;">{boxes}</div>')
    
    return '<div style="text-align:center;">' + ''.join(html_parts) + '</div>'

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
    </style>
    """, unsafe_allow_html=True)
    
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
            stage_letters = STAGES[1]['letters'].copy()
            random.shuffle(stage_letters)
            st.session_state.shuffled_letters = stage_letters
            st.session_state.game_state = 'game'
            st.session_state.game_component_key += 1
            st.rerun()
    
    st.markdown('<hr style="border: none; height: 1px; background: #ddd; margin: 1.5rem 0;">', unsafe_allow_html=True)
    st.markdown('<h2 style="text-align: center; color: #333; margin: 1.5rem 0 1rem 0; font-size: 1.2rem; font-weight: 600;">ステージ選択</h2>', unsafe_allow_html=True)
    
    # ステージ選択
    for i in range(0, len(STAGES), 4):
        cols = st.columns(4)
        for j in range(4):
            stage_num = i + j + 1
            if stage_num <= len(STAGES):
                stage_info = STAGES[stage_num]
                
                with cols[j]:
                    st.markdown(f'<div style="text-align: center; margin-bottom: 4px; color: #555; font-weight: 500; font-size: 11px;">{stage_info["name"]}</div>', unsafe_allow_html=True)
                    
                    if st.button("▶", key=f"stage_{stage_num}", use_container_width=True):
                        st.session_state.current_stage = stage_num
                        st.session_state.target_words = stage_info['words']
                        st.session_state.found_words = []
                        stage_letters = stage_info['letters'].copy()
                        random.shuffle(stage_letters)
                        st.session_state.shuffled_letters = stage_letters
                        st.session_state.game_state = 'game'
                        st.session_state.game_component_key += 1
                        st.rerun()
            else:
                with cols[j]:
                    st.empty()

# ゲーム画面
elif st.session_state.game_state == 'game':
    current_stage_info = STAGES[st.session_state.current_stage]
    
    if not st.session_state.shuffled_letters or len(st.session_state.shuffled_letters) != len(current_stage_info['letters']):
        stage_letters = current_stage_info['letters'].copy()
        random.shuffle(stage_letters)
        st.session_state.shuffled_letters = stage_letters
    
    letters = st.session_state.shuffled_letters
    num_letters = len(letters)
    
    # ヘッダー
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
        if st.session_state.current_stage < len(STAGES):
            if st.button("次へ", key="next_stage_header", use_container_width=True):
                st.session_state.current_stage += 1
                next_stage_info = STAGES[st.session_state.current_stage]
                st.session_state.target_words = next_stage_info['words']
                st.session_state.found_words = []
                stage_letters = next_stage_info['letters'].copy()
                random.shuffle(stage_letters)
                st.session_state.shuffled_letters = stage_letters
                st.session_state.game_component_key += 1
                st.rerun()
        else:
            st.empty()
    
    target_display = create_target_words_display(st.session_state.target_words, st.session_state.found_words)
    
    # 軽量化されたHTMLコンテンツ
    html_content = f"""
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
<style>
body{{margin:0;font-family:Arial;user-select:none;touch-action:none;background:#fafafa;height:100vh;}}
.circle-container{{position:relative;width:220px;height:220px;margin:20px auto;}}
.circle-button{{position:absolute;width:30px;height:30px;border-radius:50%;background:#fff;color:#333;font-size:14px;font-weight:bold;border:1px solid #333;cursor:pointer;display:flex;justify-content:center;align-items:center;}}
.selected{{background:#333!important;color:white!important;}}
#word{{text-align:center;font-size:18px;font-weight:bold;padding:10px;}}
#targets{{text-align:center;font-size:12px;padding:10px;}}
#msg{{position:fixed;top:40%;left:50%;transform:translate(-50%,-50%);background:#4CAF50;color:white;padding:10px 20px;border-radius:5px;opacity:0;transition:opacity 0.3s;}}
.show{{opacity:1!important;}}
</style>
</head>
<body>
<div id="word"></div>
<div id="targets">{target_display}</div>
<div id="msg">正解！</div>
<div class="circle-container">
"""

    # 円形ボタンの生成
    for i, letter in enumerate(letters):
        x = 110 + 65 * math.cos(2 * math.pi * i / num_letters - math.pi/2) - 15
        y = 110 + 65 * math.sin(2 * math.pi * i / num_letters - math.pi/2) - 15
        html_content += f'<div class="circle-button" data-letter="{letter}" data-index="{i}" style="left:{x}px;top:{y}px;">{letter}</div>'

    html_content += f"""
</div>
<script>
let isDragging=false,selectedLetters=[],selectedButtons=[],targetWords={json.dumps(st.session_state.target_words)},foundWords={json.dumps(st.session_state.found_words)};
const wordDiv=document.getElementById('word'),msgDiv=document.getElementById('msg');

function updateWord(){{wordDiv.textContent=selectedLetters.join('');}}

function selectButton(btn){{
if(!selectedButtons.includes(btn)){{
btn.classList.add('selected');
selectedLetters.push(btn.dataset.letter);
selectedButtons.push(btn);
updateWord();
}}
}}

function clearSelection(){{
document.querySelectorAll('.circle-button').forEach(b=>b.classList.remove('selected'));
selectedLetters=[];selectedButtons=[];updateWord();
}}

function checkWord(){{
const word=selectedLetters.join('');
if(word&&targetWords.includes(word)&&!foundWords.includes(word)){{
foundWords.push(word);
msgDiv.classList.add('show');
setTimeout(()=>msgDiv.classList.remove('show'),2000);
window.parent.postMessage({{type:'streamlit:setComponentValue',value:{{action:'word_found',word:word}}}}, '*');
return true;
}}
return false;
}}

function getButtonAt(x,y){{
let closest=null,minDist=Infinity;
document.querySelectorAll('.circle-button').forEach(btn=>{{
const rect=btn.getBoundingClientRect();
const dist=Math.sqrt(Math.pow(x-rect.left-15,2)+Math.pow(y-rect.top-15,2));
if(dist<20&&dist<minDist){{closest=btn;minDist=dist;}}
}});
return closest;
}}

document.addEventListener('mousedown',e=>{{
e.preventDefault();isDragging=true;clearSelection();
const btn=getButtonAt(e.clientX,e.clientY);
if(btn)selectButton(btn);
}});

document.addEventListener('mousemove',e=>{{
if(isDragging){{
const btn=getButtonAt(e.clientX,e.clientY);
if(btn)selectButton(btn);
}}
}});

document.addEventListener('mouseup',e=>{{
if(isDragging){{
isDragging=false;
const correct=checkWord();
setTimeout(()=>clearSelection(),correct?1000:200);
}}
}});

document.addEventListener('touchstart',e=>{{
e.preventDefault();isDragging=true;clearSelection();
const touch=e.touches[0],btn=getButtonAt(touch.clientX,touch.clientY);
if(btn)selectButton(btn);
}},{{passive:false}});

document.addEventListener('touchmove',e=>{{
if(isDragging){{
const touch=e.touches[0],btn=getButtonAt(touch.clientX,touch.clientY);
if(btn)selectButton(btn);
}}
}},{{passive:false}});

document.addEventListener('touchend',e=>{{
if(isDragging){{
isDragging=false;
const correct=checkWord();
setTimeout(()=>clearSelection(),correct?1000:200);
}}
}},{{passive:false}});

updateWord();
</script>
</body>
</html>
"""

    # HTMLコンポーネントのレンダリング
    try:
        component_value = components.html(
            html_content, 
            height=300, 
            key=f"game_component_{st.session_state.game_component_key}"
        )

        # コンポーネントからの値を処理
        if component_value is not None:
            if isinstance(component_value, dict) and component_value.get('action') == 'word_found':
                found_word = component_value.get('word')
                if (found_word and 
                    found_word in st.session_state.target_words and 
                    found_word not in st.session_state.found_words):
                    st.session_state.found_words.append(found_word)
                    st.session_state.last_update_time = time.time()
                    st.rerun()

    except Exception as e:
        st.error("ゲームの読み込み中にエラーが発生しました。ページを更新してください。")
        st.write(f"エラー詳細: {str(e)}")

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
                    stage_letters = next_stage_info['letters'].copy()
                    random.shuffle(stage_letters)
                    st.session_state.shuffled_letters = stage_letters
                    st.session_state.game_component_key += 1
                    st.rerun()
            else:
                st.balloons()
                st.success("全ステージクリア！おめでとうございます！")
                if st.button("タイトルに戻る", key="back_to_title", use_container_width=True, type="primary"):
                    st.session_state.game_state = 'title'
                    st.rerun()