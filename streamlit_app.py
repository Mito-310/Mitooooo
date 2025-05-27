import streamlit as st
from streamlit_drawable_canvas import st_canvas
import numpy as np
from PIL import Image, ImageDraw

st.title("記号をなぞってつなげる")

# キャンバスのサイズ
canvas_width = 400
canvas_height = 400

# 背景画像（記号を配置）
def generate_background():
    img = Image.new("RGB", (canvas_width, canvas_height), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    # 記号（点）を配置
    points = [(100, 100), (300, 100), (100, 300), (300, 300)]
    for p in points:
        draw.ellipse((p[0]-10, p[1]-10, p[0]+10, p[1]+10), fill=(0, 0, 0))
    
    return img

background = generate_background()

# 描画キャンバス
canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",  # 線の色
    stroke_width=5,
    stroke_color="#0000FF",
    background_image=background,
    update_streamlit=True,
    height=canvas_height,
    width=canvas_width,
    drawing_mode="freedraw",
    key="canvas"
)

# 描画データの確認（デバッグ用）
if canvas_result.json_data is not None:
    st.subheader("なぞった線のデータ:")
    st.write(canvas_result.json_data)
