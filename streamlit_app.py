import streamlit as st
import os 
# Firestore接続は後で実装します

# --- 1. 認証設定 (Secretsを使用) ---
# Secretsに設定したパスワード (st.secrets["APP_PASSWORD"]) を使用
def check_password():
    """Returns `True` if the user entered the correct password."""
    # st.secrets から APP_PASSWORD を取得し、入力されたパスワードと比較
    if st.session_state.get("password_input") == st.secrets.get("APP_PASSWORD"):
        del st.session_state["password_input"] # パスワードをセッションに保存しない
        return True
    return False

# --- 2. 認証処理 ---
# アプリの状態を管理するキー
if "password_correct" not in st.session_state:
    st.session_state["password_correct"] = False

if not st.session_state["password_correct"]:
    st.title("🔐 技術トレンド相談システム ログイン")
    
    # パスワード入力フォーム
    password_input = st.text_input("パスワード", type="password", on_change=check_password, key="password_input")
    
    if st.session_state.get("password_input") and not check_password():
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
        st.warning("🚨 RAG検索ロジックを実装します。") 
    else:
        st.error("質問を入力してください。")
        
# --- ログアウトボタン（簡易実装） ---
if st.button("ログアウト"):
    st.session_state["password_correct"] = False
    st.rerun()
