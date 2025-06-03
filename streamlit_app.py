import streamlit as st
import random
import time

# 素因数分解を行う関数
def prime_factors(n):
    i = 2
    factors = []
    while i * i <= n:
        while (n % i) == 0:
            factors.append(i)
            n //= i
        i += 1
    if n > 1:
        factors.append(n)
    return factors

# ゲームの状態を管理するクラス
class FactorGame:
    def __init__(self):
        self.score = 0
        self.level = 1
        self.time_limit = 30  # 時間制限（秒）
        self.start_time = time.time()

    # 新しい問題をランダムに生成する
    def generate_problem(self):
        number = random.randint(2, 100 * self.level)
        factors = prime_factors(number)
        return number, factors

    # ゲーム開始
    def start(self):
        st.title("素因数分解ゲーム")
        st.write("ゲームを開始します！素因数分解を学んでスコアを稼ごう！")

        # ゲーム状態を表示
        st.write(f"現在のスコア: {self.score}")
        st.write(f"レベル: {self.level}")
        st.write(f"残り時間: {max(0, self.time_limit - (time.time() - self.start_time)):.2f}秒")

        # 新しい問題を生成
        number, correct_factors = self.generate_problem()

        # ユーザー入力
        st.write(f"素因数分解してください: {number}")
        user_input = st.text_input("素因数をカンマで区切って入力してください（例: 2, 3, 5）")

        # 結果チェック
        if user_input:
            user_factors = [int(x.strip()) for x in user_input.split(',')]
            if sorted(user_factors) == sorted(correct_factors):
                self.score += 10
                self.level += 1
                st.success(f"正解！素因数分解: {correct_factors}")
            else:
                st.error(f"不正解。正しい答えは: {correct_factors}")
            # 次の問題へ
            self.start_time = time.time()

    # ゲームオーバーの判定
    def check_game_over(self):
        if time.time() - self.start_time >= self.time_limit:
            st.write("時間切れ！ゲームオーバー")
            st.write(f"最終スコア: {self.score}")
            st.stop()

def main():
    game = FactorGame()

    while True:
        game.check_game_over()
        game.start()

if __name__ == "__main__":
    main()
