import streamlit as st

st.title('あいうえお')

st.write('aaaaa')

user_name = st.text_input('名前を入力してください')

st.header('あなたの名前は'+str(user_name)+'です')