import streamlit as st

st.title('クイズ！')

st.write('日田高１年の学年カラーは？')

if st.button('青'):
    st.write('正解！')
st.button('赤')
st.button('緑')