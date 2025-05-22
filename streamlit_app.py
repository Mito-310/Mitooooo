import streamlit as st

st.title('クイズ！')

st.write('日田高１年の学年カラーは？')

if st.button('青'):
    st.write('正解！')
if st.button('赤'):
    st.write('残念...')
if st.button('緑'):
    st.write('残念...')