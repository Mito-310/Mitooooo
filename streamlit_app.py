import streamlit as st

def start_screen():
    st.title("ゲーム - スタート画面")
    st.write("このゲームでは、素因数分解を学びながら遊べます。")
    if st.button("ゲーム開始"):
        st.session_state['game_started'] = True
        st.experimental_rerun()  # 画面を更新してホーム画面へ移動

def home_screen():
    st.title("ゲーム - ホーム画面")
    st.write("ここがゲームのホーム画面です。")
    if st.button("スタート画面に戻る"):
        st.session_state['game_started'] = False
        st.experimental_rerun()

def main():
    if 'game_started' not in st.session_state:
        st.session_state['game_started'] = False

    if not st.session_state['game_started']:
        start_screen()
    else:
        home_screen()

if __name__ == "__main__":
    main()
