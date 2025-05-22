import streamlit as st

st.title('To Doリスト：')

agree=st.checkbox('朝６時に起きる')
if agree:
    st.write('えらい！')