import streamlit as st

st.title('To Doリスト：')

agree=st.checkbox('朝６時に起きる')
if agree:
    st.write('えらい！一日がんばろう！')

agree=st.checkbox('弁当を作る')
if agree:
    st.write('保冷剤入れた？')
