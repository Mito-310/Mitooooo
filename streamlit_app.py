import streamlit as st
import random
from datetime import datetime

# ページ設定
st.set_page_config(
    page_title="今日の運勢占い",
    page_icon="🔮"
)

# タイトル
st.title("🔮 今日の運勢占い")

# 現在の日付を表示
st.write(f"今日の日付: {datetime.now().strftime('%Y年%m月%d日')}")

# 運勢のリスト
fortunes = [
    {"運勢": "大吉", "説明": "絶好調！思い切った行動が吉となるでしょう。", "ラッキーカラー": "赤", "ラッキーナンバー": random.randint(1, 9)},
    {"運勢": "中吉", "説明": "良い一日になりそう。新しいことに挑戦するのも良いでしょう。", "ラッキーカラー": "青", "ラッキーナンバー": random.randint(1, 9)},
    {"運勢": "小吉", "説明": "穏やかな一日。無理せず着実に進めましょう。", "ラッキーカラー": "緑", "ラッキーナンバー": random.randint(1, 9)},
    {"運勢": "末吉", "説明": "普通の一日。慎重に行動すれば良い結果につながります。", "ラッキーカラー": "黄", "ラッキーナンバー": random.randint(1, 9)},
    {"運勢": "凶", "説明": "少し注意が必要。落ち着いて行動しましょう。", "ラッキーカラー": "紫", "ラッキーナンバー": random.randint(1, 9)}
]

# 名前入力
name = st.text_input("あなたの名前を入力してください")

# 占うボタン
if st.button("運勢を占う"):
    if name:
        st.write(f"---\n{name}さんの今日の運勢は...")
        
        # アニメーション効果
        with st.spinner("占い中..."):
            import time
            time.sleep(1)
        
        # ランダムに運勢を選択
        fortune = random.choice(fortunes)
        
        # 結果表示
        st.header(f"【{fortune['運勢']}】")
        st.write(f"✨ {fortune['説明']}")
        st.write(f"🎨 ラッキーカラー: {fortune['ラッキーカラー']}")
        st.write(f"🔢 ラッキーナンバー: {fortune['ラッキーナンバー']}")
        
        # 運勢に応じたアドバイス表示
        if fortune['運勢'] in ['大吉', '中吉']:
            st.success("今日は積極的に行動するといいでしょう！")
        elif fortune['運勢'] in ['小吉', '末吉']:
            st.info("無理せず、着実に進めていきましょう。")
        else:
            st.warning("今日は慎重に行動することをおすすめします。")
    else:
        st.error("名前を入力してください！")