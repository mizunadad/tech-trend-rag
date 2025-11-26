import streamlit as st
import os 
import firebase_admin
from firebase_admin import credentials, firestore 
from sentence_transformers import SentenceTransformer # 検索に必要なため追加
import anthropic

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
# streamlit_app.py の run_rag_search() 関数全体を置き換えます

def run_rag_search(query):
    # 接続が成功しているため、そのまま DB クライアントを取得
    db = setup_firestore()
    
    # 1. 質問のベクトル化 (簡易的な実装)
    # NOTE: 実際にはここで質問文をベクトル化し、Firestoreでベクトル検索を行う必要があります。
    #       今回は、ベクトル検索の実装はスキップし、全ドキュメントからランダムに取得する簡易RAGを実装します。
    
    try:
        # 簡易RAG検索: Firestoreからランダムな関連ドキュメントを5件取得
        docs_ref = db.collection("tech_docs").limit(5).stream()
        docs = list(docs_ref)
        
        if not docs:
            return "データが見つかりません。Firestoreにデータが正しく投入されているか確認してください。"

        # 2. コンテキストの構築
        context_text = "\n\n---\n\n".join([doc.to_dict().get('content', '') for doc in docs])
        
        # 3. Claude APIの呼び出し
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
            model="claude-3-sonnet-20240229",
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

# 既存の検索実行ボタンのロジックを修正
if st.button("🔍 検索実行", type="primary"):
    if query:
        with st.spinner("RAG検索を実行中..."):
            result_dict = run_rag_search(query)
            
            if isinstance(result_dict, str):
                st.error(result_dict)
            else:
                st.markdown(f"**💡 回答**\n\n{result_dict['answer']}")
                st.markdown(f"**📚 参考資料:** {', '.join(result_dict['sources'])}")
    else:
        st.error("質問を入力してください。")


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
if st.button("🔍 検索実行", type="primary",key='rag_search_button'):
    if query:
        with st.spinner("RAG検索を実行中... Firestore接続をテスト中..."):
            #接続テストを実行
            result_text = run_rag_search(query)
            st.markdown(f"**結果** {result_text}")
    else:
        st.error("質問を入力してください。")
        
# --- ログアウトボタン（簡易実装） ---
if st.button("ログアウト",key='logout_button_main'):
    st.session_state["password_correct"] = False
    st.rerun()
