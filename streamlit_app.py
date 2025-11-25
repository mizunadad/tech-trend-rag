import streamlit as st
import os # 環境変数アクセス用 (今回のパスワード保護で使用)
# Note: 既存の RAG ロジック (firebase_admin, anthropic, sentence_transformers) は
#       この後、requirements.txt に基づいてインストールされます。

# --- 1. 認証設定 (Secretsを使用) ---
# Streamlit Cloudの管理画面で APP_PASSWORD を設定してください
def check_password():
    """Returns `True` if the user entered the correct password."""
    # st.secrets から APP_PASSWORD を取得し、入力されたパスワードと比較
    if st.session_state.get("password") == st.secrets.get("APP_PASSWORD"):
        del st.session_state["password"]  # パスワードをセッションに保存しない
        return True
    return False

# --- 2. 認証処理 ---
# st.session_state は、アプリの状態を管理するためのStreamlitの機能です
if "password_correct" not in st.session_state:
    st.session_state["password_correct"] = False

if not st.session_state["password_correct"]:
    st.title("🔐 技術トレンド相談システム ログイン")
    
    # パスワード入力フォーム
    password_input = st.text_input("パスワード", type="password", key="password")
    
    # EnterキーまたはLoginボタンが押された時の処理
    if st.button("Login") or password_input:
        if check_password():
            st.session_state["password_correct"] = True
            st.rerun() # 認証成功後、アプリを再実行してメイン画面へ
        else:
            st.error('パスワードが間違っています。')
            
    st.stop() # パスワードが合わない場合は、ここで処理を停止

# --- 3. 認証成功後のメインコンテンツ ---
# この下にRAGロジックが続きます

st.title("🔬 技術トレンド相談システム (Streamlit版)")
st.markdown("#### 家族それぞれのキャリアサポートを目的としたRAGシステムです。")

# 🚨 RAGロジック（未実装部分）
query = st.text_area("質問を入力してください", height=100)
if st.button("🔍 検索実行", type="primary"):
    if query:
        st.info(f"質問内容: {query}")
        st.warning("🚨 RAG検索ロジックは未実装です。") 
    else:
        st.error("質問を入力してください。")

# --- ログアウトボタン（簡易実装） ---
if st.button("ログアウト"):
    st.session_state["password_correct"] = False
    st.rerun()
