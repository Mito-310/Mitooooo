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

# 簡易英単語辞書
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

# レベルごとに3単語出題
words_per_level = 3

# ゲームの状態を保存
if 'level' not in st.session_state:
    st.session_state.level = 0
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'found_words' not in st.session_state:
    st.session_state.found_words = []
if 'current_selection' not in st.session_state:
    st.session_state.current_selection = []

# 出題単語
word_list = words[st.session_state.level * words_per_level:(st.session_state.level + 1) * words_per_level]

# 使える文字は出題単語に含まれる文字の集合
letters = list(set(''.join(word_list)))

st.title("Word Connect")

st.write(f"レベル: {st.session_state.level + 1}")
st.write(f"スコア: {st.session_state.score}")

st.write("## 使える文字")
cols = st.columns(len(letters))
for i, letter in enumerate(letters):
    if cols[i].button(letter):
        st.session_state.current_selection.append(letter)

# 現在の選択単語
current_word = ''.join(st.session_state.current_selection)
st.write(f"### 選択中の単語: **{current_word}**")

def can_form_word(word, letters_available):
    # 入力単語の各文字がletters_availableに十分あるかチェック
    letters_copy = list(letters_available)
    for c in word:
        if c in letters_copy:
            letters_copy.remove(c)
        else:
            return False
    return True

# 提出ボタン
if st.button("単語を提出する"):
    # 入力単語がdictionaryにあるか、かつ使える文字の範囲内か、かつ未発見かを判定
    if current_word in dictionary and can_form_word(current_word, letters) and current_word not in st.session_state.found_words:
        st.success(f"正解！『{current_word}』を見つけました。")
        st.session_state.found_words.append(current_word)
        st.session_state.score += 1
    else:
        st.error("不正解か既に見つけた単語です。")
    st.session_state.current_selection = []

# 選択リセット
if st.button("選択をリセット"):
    st.session_state.current_selection = []

# 見つけた単語一覧
st.write("## 見つけた単語")
if st.session_state.found_words:
    st.write(", ".join(st.session_state.found_words))
else:
    st.write("まだ単語は見つかっていません。")

# レベルクリア判定（word_listに含まれる単語は必須、部分単語はボーナス扱い）
required_words_found = all(word in st.session_state.found_words for word in word_list)
if required_words_found:
    st.success("🎉 レベルクリア！次のレベルへ進みます。")
    if st.button("次のレベルへ"):
        st.session_state.level += 1
        st.session_state.found_words = []
        st.session_state.current_selection = []
        st.experimental_rerun()

# レベルが最後まで到達したらメッセージ
if st.session_state.level >= len(words) // words_per_level:
    st.balloons()
    st.write("すべてのレベルをクリアしました！おめでとうございます！")
