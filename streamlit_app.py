import streamlit as st
import language_tool_python

# 英作文を添削する関数
def check_grammar(text):
    tool = language_tool_python.LanguageTool('en-US')
    matches = tool.check(text)
    corrected_text = language_tool_python.utils.correct(text, matches)
    return corrected_text, matches

# Streamlitアプリケーション
def main():
    st.title("英作文の添削アプリ")
    
    # ユーザーに英作文を入力してもらう
    user_input = st.text_area("英作文を入力してください:")
    
    if user_input:
        # 文法チェックを実行
        corrected_text, matches = check_grammar(user_input)
        
        # 添削結果を表示
        st.subheader("添削結果")
        st.write("**修正後の文**:")
        st.write(corrected_text)
        
        st.write("\n**修正内容**:")
        for match in matches:
            st.write(f"【{match.ruleId}】{match.message}")
            st.write(f" 修正案: {match.replacements}")
            st.write("")

# Streamlitアプリを実行
if __name__ == "__main__":
    main()



