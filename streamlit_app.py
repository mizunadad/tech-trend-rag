import streamlit as st
import os 
import firebase_admin
from firebase_admin import credentials, firestore 
from sentence_transformers import SentenceTransformer # 検索に必要なため追加

# Firestore接続のためのユーティリティ関数
# この関数は、st.secrets["firebase"] から鍵を取得し、Firebase Admin SDKを初期化します。
@st.cache_resource # 👈 Streamlitで接続をキャッシュするデコレータ
def setup_firestore():
    # Firestore接続に必要なライブラリをインポート
    import firebase_admin
    from firebase_admin import credentials, firestore
    import json

    # 既に初期化済みでなければ、st.secretsから認証情報を読み込み初期化
    if not firebase_admin._apps:
        # 🚨 修正箇所: Secretsから JSON文字列を読み込み、Python辞書に変換
        cert_json_string = st.secrets["firebase"]["cert_json"]
        cert_dict = json.loads(cert_json_string) # JSON文字列をPython辞書に変換

        # 認証情報を辞書として使用
        cred = credentials.Certificate(cert_dict)
        firebase_admin.initialize_app(cred)

    return firestore.client()

# --- 認証成功後のメインコンテンツ内を修正 ---

# 🚨 RAG検索ロジックのプレースホルダー
def run_rag_search(query):
    # 接続テストとデータ存在確認
    try:
        # st.cache_resourceによって接続が使い回されます
        db = setup_firestore() 
        
        # 簡易データ確認（'tech_docs'コレクションの最初の5件を取得）
        doc_count = len(list(db.collection("tech_docs").limit(5).stream()))
        
        if doc_count > 0:
            return f"✅ Firestore接続成功！ 'tech_docs' コレクションにデータ {doc_count} 件以上を確認しました。次はRAG検索を実装します。"
        else:
            return "⚠️ Firestore接続成功。しかし 'tech_docs' コレクションにデータが見つかりません。データの再投入が必要です。"
            
    except Exception as e:
        return f"❌ Firestore接続失敗: {e}"



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

    # 🚨 修正箇所: on_changeイベントを使わず、フォームとして処理します
    with st.form("login_form"):
        # st.session_state["password_input"]に値が入る
        password_input = st.text_input("パスワード", type="password", key="password_input_key") 
        submitted = st.form_submit_button("Login")

        if submitted:
            # 入力値をセッションに一時保存し、check_passwordを呼び出す
            st.session_state["password_input"] = password_input
            
            if check_password():
                st.session_state["password_correct"] = True
                st.rerun() # 認証成功後、アプリを再実行してメイン画面へ
            else:
                st.error('パスワードが間違っています。')
            
    st.stop()
# --- 3. 認証成功後のメインコンテンツ ---
# この下にRAGロジックが続きます

st.title("🔬 技術トレンド相談システム (Streamlit版)")
st.markdown("#### 家族それぞれのキャリアサポートを目的としたRAGシステムです。")

# 🚨 RAGロジック（未実装部分）
query = st.text_area("質問を入力してください", height=100)
if st.button("🔍 検索実行", type="primary"):
    if query:
        with st.spinner("RAG検索を実行中... Firestore接続をテスト中..."):
            #接続テストを実行
            result_text = run_rag_search(query)
            st.markdown(f"**結果** {result_text}")
    else:
        st.error("質問を入力してください。")
        
# --- ログアウトボタン（簡易実装） ---
if st.button("ログアウト"):
    st.session_state["password_correct"] = False
    st.rerun()
