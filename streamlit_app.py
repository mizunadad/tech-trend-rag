import streamlit as st
import os 
import json
import firebase_admin
from firebase_admin import credentials, firestore
from sentence_transformers import SentenceTransformer
import anthropic

# --- 1. Firestore接続のためのユーティリティ関数 ---
@st.cache_resource
def setup_firestore():
    # 接続に必要なライブラリは既にインポート済み

    if not firebase_admin._apps:
        # Secretsから JSON文字列を読み込み、Python辞書に変換
        cert_json_string = st.secrets["firebase"]["cert_json"] 
        cert_dict = json.loads(cert_json_string) 

        # 認証情報を辞書として使用
        cred = credentials.Certificate(cert_dict)
        firebase_admin.initialize_app(cred)
        
    return firestore.client()

# --- 2. RAG検索ロジック ---
def run_rag_search(query):
    db = setup_firestore()
    
    try:
        # 簡易RAG検索: Firestoreからランダムな関連ドキュメントを5件取得
        docs_ref = db.collection("tech_docs").limit(5).stream()
        docs = list(docs_ref)
        
        if not docs:
            return "データが見つかりません。Firestoreにデータが正しく投入されているか確認してください。"

        # 2. コンテキストの構築
        context_text = "\n\n---\n\n".join([doc.to_dict().get('content', '') for doc in docs])
        
        # 3. Claude APIの呼び出し
        # SecretsからCLAUDE_API_KEYを取得
        client = anthropic.Anthropic(api_key=st.secrets["CLAUDE_API_KEY"])
        
        prompt = f"""
        あなたは家族向け技術トレンド相談エキスパートです。以下の技術情報を参考に、質問に回答してください。
        【技術情報】
        {context_text}
        【質問】
        {query}

        【回答形式】
        - 簡潔で分かりやすく
        - 必ず具体的な技術名と出典（文書タイトル）を挙げる
        """
        
        response = client.messages.create(
            model="claude-3-5-sonnet", # 安定版エイリアス
            max_tokens=2000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        # 4. 結果の整形と返却
        sources = [doc.to_dict().get('title', '不明') for doc in docs]
        
        return {
            "answer": response.content[0].text,
            "sources": sources
        }
            
    except Exception as e:
        # Claude APIキーが無効、またはFirestore接続が切れた場合
        return f"❌ RAG検索失敗: サーバー内部エラーが発生しました ({e})"

# --- 3. 認証ロジック ---
def check_password():
    """Returns `True` if the user entered the correct password."""
    # Secretsから APP_PASSWORD を取得し、入力されたパスワードと比較
    if st.session_state.get("password_input") == st.secrets.get("APP_PASSWORD"):
        del st.session_state["password_input"] 
        return True
    return False

if "password_correct" not in st.session_state:
    st.session_state["password_correct"] = False

if not st.session_state["password_correct"]:
    st.title("🔐 技術トレンド相談システム ログイン")
    
    with st.form("login_form"):
        st.text_input("パスワード", type="password", key="password_input")
        submitted = st.form_submit_button("Login")

        if submitted:
            if check_password():
                st.session_state["password_correct"] = True
                st.rerun() 
            else:
                st.error('パスワードが間違っています。')
            
    st.stop() # パスワードが合わない場合は、ここで処理を停止

# --- 4. 認証成功後のメインコンテンツ ---

st.title("🔬 技術トレンド相談システム (Streamlit版)")
st.markdown("#### 家族それぞれのキャリアサポートを目的としたRAGシステムです。")

# 🚨 修正箇所: ここで st.text_area を定義することで、queryがグローバルスコープで使えるようにする
query = st.text_area("質問を入力してください", height=100) 

# 🚨 修正箇所: ボタンは一つだけ定義し、キーを追加
if st.button("🔍 検索実行", type="primary", key='rag_search_button'):
    if query:
        with st.spinner("RAG検索を実行中..."):
            result = run_rag_search(query)
            
            if isinstance(result, str):
                st.error(result)
            else:
                st.markdown(f"**💡 回答**\n\n{result['answer']}")
                st.markdown(f"**📚 参考資料:** {', '.join(result['sources'])}")
    else:
        st.error("質問を入力してください。")
        
# --- ログアウトボタン ---
if st.button("ログアウト", key='logout_button_main'):
    st.session_state["password_correct"] = False
    st.rerun()
