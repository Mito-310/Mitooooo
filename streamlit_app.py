import streamlit as st
import random

# 単語リスト
words = [
    'admit', 'adventure', 'afford', 'appreciate', 'medicine', 'population', 'rely', 'conversation',
    'exactly', 'spirit', 'treat', 'anxious', 'unless', 'frankly', 'whisper', 'appointment',
    'decoration', 'decrease', 'despite', 'explanation', 'explorer', 'furniture', 'further',
    'charity', 'spare', 'forecast', 'audience', 'impress', 'apply', 'instruction', 'award',
    'destroy', 'generally', 'contain', 'sweep', 'ideal', 'chew', 'modern', 'author', 'nation',
    'ceremony', 'direction', 'issue', 'silly', 'eventually', 'ancestor', 'memorize', 'corporation',
    'product', 'citizen', 'prove', 'commercial', 'disappoint', 'journey', 'originally', 'soil',
    'fantastic', 'attractive', 'prevent', 'examination', 'role', 'courage', 'silence', 'confident',
    'emotion', 'nod', 'recommend', 'surround', 'hire', 'chemistry', 'require', 'forgive', 'stare',
    'exhibit', 'suggestion', 'constant', 'exhibition', 'operation', 'receipt', 'survive', 'otherwise',
    'suitable', 'avenue', 'earn', 'enemy', 'achieve', 'advertisement', 'instrument', 'organize',
    'unfortunately', 'describe', 'employ', 'examine', 'harmful', 'importance', 'region', 'relation',
    'rough', 'remind', 'surface'
]

# 単語辞書
dictionary = set([
    'ad', 'it', 'admit', 'venture', 'afford', 'appreciate', 'med', 'medicine', 'pop', 'population',
    'rely', 'con', 'conversation', 'exact', 'exactly', 'spirit', 'treat', 'anxious', 'unless',
    'frank', 'frankly', 'whisper', 'appointment', 'decoration', 'decrease', 'despite',
    'explain', 'explanation', 'explore', 'explorer', 'furnish', 'furniture', 'further',
    'charity', 'spare', 'forecast', 'audience', 'impress', 'apply', 'instruct', 'instruction',
    'award', 'destroy', 'generally', 'contain', 'sweep', 'ideal', 'chew', 'modern', 'author',
    'nation', 'ceremony', 'direction', 'issue', 'silly', 'event', 'eventually', 'ancestor',
    'memorize', 'corporation', 'product', 'citizen', 'prove', 'commercial', 'disappoint',
    'journey', 'original', 'originally', 'soil', 'fantastic', 'attractive', 'prevent',
    'examination', 'role', 'courage', 'silence', 'confident', 'emotion', 'nod', 'recommend',
    'surround', 'hire', 'chemistry', 'require', 'forgive', 'stare', 'exhibit', 'suggestion',
    'constant', 'exhibition', 'operation', 'receipt', 'survive', 'otherwise', 'suitable',
    'avenue', 'earn', 'enemy', 'achieve', 'advertisement', 'instrument', 'organize',
    'unfortunately', 'describe', 'employ', 'examine', 'harmful', 'importance', 'region',
    'relation', 'rough', 'remind', 'surface', 'am', 'me', 'in', 'on', 'no', 'or', 'an'
])

# レベル管理
words_per_level = 3
if 'level' not in st.session_state:
    st.session_state.level = 0
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'found_words' not in st.session_state:
    st.session_state.found_words = []
if 'current_selection' not in st.session_state:
    st.session_state.current_selection = []

# 現在の単語セット
word_list = words[st.session_state.level * words_per_level:(st.session_state.level + 1) * words_per_level]
letters = list(set(''.join(word_list)))

# タイトルと情報表示
st.title("Word Connect")
st.write(f"レベル: {st.session_state.level + 1}")
st.write(f"スコア: {st.session_state.score}")

# CSS: 丸いボタンスタイル
st.markdown("""
    <style>
    div.stButton > button {
        border-radius: 50%;
        height: 60px;
        width: 60px;
        margin: 4px;
        font-weight: bold;
        font-size: 20px;
        background-color: #f2f2f2;
        color: #333;
        border: 2px solid #999;
        transition: all 0.2s ease-in-out;
    }
    div.stButton > button:hover {
        background-color: #ddd;
        border-color: #666;
    }
    </style>
""", unsafe_allow_html=True)

# アルファベットボタンを表示
st.write("## 使える文字")
cols = st.columns(len(letters))
for i, letter in enumerate(letters):
    if cols[i].button(letter, key=f"letter_{i}"):
        st.session_state.current_selection.append(letter)

# 選択中の単語表示
current_word = ''.join(st.session_state.current_selection)
st.write(f"### 選択中の単語: **{current_word}**")

# 単語が作れるかの判定関数
def can_form_word(word, letters_available):
    letters_copy = list(letters_available)
    for c in word:
        if c in letters_copy:
            letters_copy.remove(c)
        else:
            return False
    return True

# 提出処理
if st.button("提出"):
    if current_word in dictionary and can_form_word(current_word, letters) and current_word not in st.session_state.found_words:
        st.success(f"正解！『{current_word}』を見つけました。")
        st.session_state.found_words.append(current_word)
        st.session_state.score += 1
    else:
        st.error("不正解か既に見つけた単語です。")
    st.session_state.current_selection = []

# リセットボタン
if st.button("reset"):
    st.session_state.current_selection = []

# 発見済み単語
st.write("## My辞書")
if st.session_state.found_words:
    st.write(", ".join(st.session_state.found_words))
else:
    st.write("まだ単語は見つかっていません。")

# レベルクリア判定
required_words_found = all(word in st.session_state.found_words for word in word_list)
if required_words_found:
    st.success("🎉 レベルクリア！次のレベルへ進みます。")
    if st.button("次のレベルへ"):
        st.session_state.level += 1
        st.session_state.found_words = []
        st.session_state.current_selection = []
        st.experimental_rerun()

# 全レベル終了メッセージ
if st.session_state.level >= len(words) // words_per_level:
    st.balloons()
    st.write("すべてのレベルをクリアしました！おめでとうございます！")
