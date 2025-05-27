import streamlit as st
from streamlit_drawable_canvas import st_canvas

st.title("四角を線でつなごう")

# キャンバスのサイズ
canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",  # 四角の塗り色
    stroke_width=2,
    background_color="#fff",
    height=400,
    width=600,
    drawing_mode="freedraw",  # または "rect" や "line"
    key="canvas"
)

if canvas_result.json_data is not None:
    st.write("描画データ:")
    st.json(canvas_result.json_data)