import streamlit as st
import random

# 英検2級頻出単語リスト（例）
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

# ゲームの状態を保存
if 'level' not in st.session_state:
    st.session_state.level = 0
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'found_words' not in st.session_state:
    st.session_state.found_words = []
if 'current_selection' not in st.session_state:
    st.session_state.current_selection = []

# 現在の単語リストと文字セット
word_list = words[st.session_state.level:st.session_state.level + 3]  # 各レベルで3単語を出題
letters = list(set(''.join(word_list)))  # 重複文字は一度だけ

st.title("🧩 英検2級 単語並び替えパズル")

st.write(f"レベル: {st.session_state.level + 1}")
st.write(f"スコア: {st.session_state.score}")

st.write("## 使える文字")
cols = st.columns(len(letters))
for i, letter in enumerate(letters):
    if cols[i].button(letter):
        st.session_state.current_selection.append(letter)

# 現在の選択文字を表示
current_word = ''.join(st.session_state.current_selection)
st.write(f"### 選択中の単語: **{current_word}**")

# 提出ボタン
if st.button("単語を提出する"):
    if current_word in word_list and current_word not in st.session_state.found_words:
        st.success(f"正解！『{current_word}』を見つけました。")
        st.session_state.found_words.append(current_word)
        st.session_state.score += 1
    else:
        st.error("不正解か既に見つけた単語です。")
    st.session_state.current_selection = []

# 選択リセットボタン
if st.button("選択をリセット"):
    st.session_state.current_selection = []

# 見つけた単語一覧
st.write("## 見つけた単語")
if st.session_state.found_words:
    st.write(", ".join(st.session_state.found_words))
else:
    st.write("まだ単語は見つかっていません。")

# レベルクリア判定
if set(st.session_state.found_words) == set(word_list):
    st.success("🎉 レベルクリア！次のレベルへ進みます。")
    if st.button("次のレベルへ"):
        st.session_state.level += 1
        st.session_state.found_words = []
        st.session_state.current_selection = []
        st.experimental_rerun()

# レベルが最後まで到達したらメッセージ
if st.session_state.level >= len(words) // 3:
    st.balloons()
    st.write("すべてのレベルをクリアしました！おめでとうございます！")
