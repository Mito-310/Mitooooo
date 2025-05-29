import streamlit as st
import base64
import json
from PIL import Image
from io import BytesIO
import numpy as np

# --- 記号の座標と正しい順序 ---
symbols = {
    "circle": {"position": (100, 100), "file": "circle.png"},
    "triangle": {"position": (300, 100), "file": "circle copy.png"},
    "square": {"position": (200, 300), "file": "circle copy2.png"},
}
correct_order = ["circle", "triangle", "square"]

st.title("記号をなぞってつなげる")

# --- JavaScript用に画像をbase64でエンコード ---
def image_to_base64(img_path):
    with open(img_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# --- キャンバスサイズ ---
width, height = 400, 400

# --- Canvas表示（JavaScript + HTML） ---
images_js = []
for name, data in symbols.items():
    img_b64 = image_to_base64(data["file"])
    x, y = data["position"]
    images_js.append(f"""
        let img_{name} = new Image();
        img_{name}.src = "data:image/png;base64,{img_b64}";
        img_{name}.onload = () => ctx.drawImage(img_{name}, {x - 20}, {y - 20}, 40, 40);
    """)

canvas_code = f"""
<canvas id="myCanvas" width="{width}" height="{height}" style="border:1px solid #000;"></canvas>
<script>
let canvas = document.getElementById("myCanvas");
let ctx = canvas.getContext("2d");
let drawing = false;
let points = [];

canvas.addEventListener("mousedown", function(e) {{
    drawing = true;
    points.push([]);
}});

canvas.addEventListener("mouseup", function(e) {{
    drawing = false;
    window.parent.postMessage({{ type: 'canvas_points', points: points }}, "*");
}});

canvas.addEventListener("mousemove", function(e) {{
    if (!drawing) return;
    let rect = canvas.getBoundingClientRect();
    let x = e.clientX - rect.left;
    let y = e.clientY - rect.top;
    points[points.length - 1].push([x, y]);

    if (points.length > 0 && points[points.length - 1].length > 1) {{
        let len = points[points.length - 1].length;
        let prev = points[points.length - 1][len - 2];
        ctx.beginPath();
        ctx.moveTo(prev[0], prev[1]);
        ctx.lineTo(x, y);
        ctx.stroke();
    }}
}});

{''.join(images_js)}
</script>
"""

st.components.v1.html(canvas_code, height=450)

# --- JavaScriptから座標データを受け取る ---
points_data = st.experimental_get_query_params().get("points")

if "js_points" not in st.session_state:
    st.session_state.js_points = None

# --- JavaScriptとの通信（iframe経由） ---
st.markdown("""
<script>
window.addEventListener("message", (event) => {
    if (event.data.type === "canvas_points") {
        const points_json = JSON.stringify(event.data.points);
        fetch(window.location.href.split("?")[0] + "?points=" + encodeURIComponent(points_json))
            .then(() => location.reload());
    }
});
</script>
""", unsafe_allow_html=True)

# --- 座標から記号に対応する順序を認識 ---
def recognize_order(points):
    detected = []
    for stroke in points:
        for x, y in stroke:
            for name, data in symbols.items():
                sx, sy = data["position"]
                if (x - sx) ** 2 + (y - sy) ** 2 < 25**2:
                    if name not in detected:
                        detected.append(name)
    return detected

# --- 判定 ---
if points_data:
    try:
        decoded = json.loads(base64.b64decode(points_data[0]).decode())
        order = recognize_order(decoded)
        st.write("なぞった順序:", order)

        if order == correct_order:
            st.success("正しい順序でつなげました！")
        else:
            st.warning("順番が違います。もう一度試してください。")

    except Exception as e:
        st.error(f"解析エラー: {e}")


