import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
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
# streamlit_app.py の run_rag_search() 関数全体を置き換えます
# setup_firestore() はそのままにしておいてください

@st.cache_resource
def load_embedding_model():
    # 以前、データ投入で使用したMiniLMモデルをロード
    return SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

def run_rag_search(query):
    db = setup_firestore()
    model = load_embedding_model() # Embeddingモデルのロード
    
    try:
        # 1. 質問のベクトル化
        query_embedding = model.encode(query)
        
        # 2. 全Firestoreドキュメントの取得（メモリにロード）
        # NOTE: 700件程度ならメモリにロード可能ですが、データが増えたら専用DBが必要です。
        all_docs = []
        for doc in db.collection("tech_docs").stream():
            data = doc.to_dict()
            data['doc_id'] = doc.id
            all_docs.append(data)

        if not all_docs:
            return "データが見つかりません。"

        # 3. 類似度計算とTop-5の選択
        # Firestoreの embedding（リスト形式）をnumpy配列に変換
        doc_embeddings = np.array([doc['embedding'] for doc in all_docs])
        
        # コサイン類似度を計算
        similarities = cosine_similarity(query_embedding.reshape(1, -1), doc_embeddings).flatten()
        
        # 類似度の高い順にインデックスを取得
        top_indices = np.argsort(similarities)[::-1][:5] # Top 5
        top_docs = [all_docs[i] for i in top_indices]

        # 4. コンテキストの構築とClaude API呼び出し (変更なし)
        context_text = "\n\n---\n\n".join([doc.get('content', '') for doc in top_docs])
        
        # Claude API呼び出し... (以下、以前のコードと同じ)
        client = anthropic.Anthropic(api_key=st.secrets["CLAUDE_API_KEY"])
        
        prompt = f"""...""" # プロンプトは省略
        
        response = client.messages.create(
            model="claude-3-haiku-20240307", # 👈 動作確認済みのHaikuを使用
            max_tokens=2000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        # 5. 結果の整形と返却
        sources = [doc.get('title', '不明') for doc in top_docs] 
        return {
            "answer": response.content[0].text,
            "sources": sources
        }
            
    except Exception as e:
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
