import streamlit as st
import os 
import json
import firebase_admin
from firebase_admin import credentials, firestore
from sentence_transformers import SentenceTransformer
import anthropic
import numpy as np
import pandas as pd # 👈 データ表示用にpandasを追加
from sklearn.metrics.pairwise import cosine_similarity

# --- 1. Firestore接続のためのユーティリティ関数 ---
@st.cache_resource
def setup_firestore():
    if not firebase_admin._apps:
        cert_json_string = st.secrets["firebase"]["cert_json"] 
        cert_dict = json.loads(cert_json_string) 
        cred = credentials.Certificate(cert_dict)
        firebase_admin.initialize_app(cred)
    return firestore.client()

# --- 2. RAG検索ロジック (フィルター機能付き) ---
@st.cache_resource
def load_embedding_model():
    return SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

def run_rag_search(query, selected_categories):
    db = setup_firestore()
    model = load_embedding_model()
    
    try:
        query_embedding = model.encode(query)
        
        # 全ドキュメント取得
        # NOTE: データ量が増えた場合は、ここでFirestoreクエリによる事前フィルタリングを検討します
        all_docs = []
        for doc in db.collection("tech_docs").stream():
            data = doc.to_dict()
            data['doc_id'] = doc.id
            # カテゴリフィルタリング
            if data.get('category') in selected_categories:
                all_docs.append(data)

        if not all_docs:
            return "条件に一致するデータが見つかりません。サイドバーのフィルタ設定を確認してください。"

        # 類似度計算
        doc_embeddings = np.array([doc['embedding'] for doc in all_docs])
        similarities = cosine_similarity(query_embedding.reshape(1, -1), doc_embeddings).flatten()
        
        top_indices = np.argsort(similarities)[::-1][:5]
        top_docs = [all_docs[i] for i in top_indices]

        # コンテキスト構築
        context_text = "\n\n---\n\n".join([doc.get('content', '') for doc in top_docs])
        
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
            model="claude-3-haiku-20240307",
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        sources = [doc.get('title', '不明') for doc in top_docs]
        
        return {
            "answer": response.content[0].text,
            "sources": sources,
            "context": context_text
        }
            
    except Exception as e:
        return f"❌ RAG検索失敗: サーバー内部エラーが発生しました ({e})"


# --- 新機能: 未来の名刺生成ロジック ---
def generate_future_career(topic):
    client = anthropic.Anthropic(api_key=st.secrets["CLAUDE_API_KEY"])
    
    prompt = f"""
    You are a visionary career consultant in the year 2035.
    Based on the technology topic: '{topic}', create a fictional, futuristic job profile.
    
    Output format (JSON):
    {{
        "job_title": "Cool sounding job title (English & Japanese)",
        "estimated_salary": "Annual salary in 2035 (JPY)",
        "required_skills": ["Skill 1", "Skill 2", "Skill 3"],
        "mission": "A short, inspiring mission statement for this job."
    }}
    Only output the JSON.
    """
    
    try:
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}]
        )
        # JSON部分だけを抽出してパースする簡易処理
        import json
        content = response.content[0].text
        # 簡易的にJSON部分を探す（{から}まで）
        json_str = content[content.find("{"):content.rfind("}")+1]
        return json.loads(json_str)
    except Exception as e:
        return None


# --- 3. データ全件取得関数 (カタログ用) ---
@st.cache_data(ttl=600) # 10分間キャッシュ
def get_all_data_as_df():
    db = setup_firestore()
    docs_list = []
    for doc in db.collection("tech_docs").stream():
        d = doc.to_dict()
        # 表示に必要な項目だけ抽出
        docs_list.append({
            "Title": d.get('title', ''),
            "Category": d.get('category', ''),
            # "Content": d.get('content', '')[:100] + "..." # コンテンツ冒頭
        })
    return pd.DataFrame(docs_list)

# --- 4. 認証ロジック ---
def check_password():
    if st.session_state.get("password_input") == st.secrets.get("APP_PASSWORD"):
        del st.session_state["password_input"] 
        return True
    return False

if "password_correct" not in st.session_state:
    st.session_state["password_correct"] = False

if not st.session_state["password_correct"]:
    st.title("⚔️ CAREER DATA VAULT: AUTH")
    st.markdown("##### 次世代戦略AIへアクセスするには、認証が必要です。")
    
    with st.form("login_form"):
        st.text_input("パスワード", type="password", key="password_input")
        submitted = st.form_submit_button("Login")

        if submitted:
            if check_password():
                st.session_state["password_correct"] = True
                st.rerun() 
            else:
                st.error('パスワードが間違っています。')
            
    st.stop() 

# --- 5. メインアプリ画面 (サイドバー付) ---

# サイドバー設定
st.sidebar.title("🔧 Control Panel")

# モード選択
app_mode = st.sidebar.radio("モード選択", ["💬 AIチャット (RAG)", "📚 データカタログ一覧"])

# ソースフィルター設定 (実際のフォルダ名に合わせてマッピング)
# gartner_2025, nikkei_bp_2025_2035 は scripts/build_vector_db.py で入れた category 名
CATEGORY_MAPPING = {
    "Gartner Hype Cycle 2025": "gartner_2025",
    "日経BP 技術トレンド": "nikkei_bp_2025_2035"
}

st.sidebar.markdown("---")
st.sidebar.subheader("🔍 検索対象ソース")
selected_labels = st.sidebar.multiselect(
    "分析対象を選択",
    options=list(CATEGORY_MAPPING.keys()),
    default=list(CATEGORY_MAPPING.keys()) # デフォルトは全選択
)
# 選択されたラベルから実際のカテゴリ名リストに変換
selected_categories = [CATEGORY_MAPPING[label] for label in selected_labels]


# --- 画面分岐 ---

if app_mode == "💬 AIチャット (RAG)":
    st.title("🧬 NEXT-GEN CAREER BRAIN")
    st.markdown("#### **Generate Your Future Roadmap. Your Personal Growth Strategy AI.**")
    st.markdown("---")
    st.markdown("##### **[ACCESS GRANTED]**。KNOWLEDGE SYSTEM READY FOR QUERY.")
    st.markdown("---")

    query = st.text_area("Enter Your Question ...🤣日本語でええよ🤣", height=100)

    if st.button("🔍 Research Techs ", type="primary", key='rag_search_button'):
        if not selected_categories:
            st.error("⚠️ 検索対象ソースが選択されていません。サイドバーで選択してください。")
        elif query:
            with st.spinner("Analyzing Data Feeds... Standby for Analysis."):
                result = run_rag_search(query, selected_categories) # フィルターを渡す
                
                if isinstance(result, str):
                    st.error(result)
                else:
                    st.markdown(f"**💡 回答**\n\n{result['answer']}")
                    st.markdown("---")
                    st.markdown(f"**📚 参照された資料:** {', '.join(result['sources'])}") 
                    
                    with st.expander("📄 参照された原文コンテンツを確認する"):
                        st.code(result['context'], language="markdown")
                    # 🚨 === ここから追加：未来の名刺機能 === 🚨
                    st.markdown("---")
                    st.markdown("### 🔮 Future Career Analysis")
                    if st.button("🃏 この技術で「2035年の未来の名刺」を作る", key="future_card_btn"):
                        with st.spinner("Generating Future Profile..."):
                            card_data = generate_future_career(query)

                            if card_data:
                                # 名刺風のデザイン表示
                                st.success("✅ 2035年のキャリア予測が完了しました")

                                # カラムを使ってレイアウト
                                col1, col2 = st.columns([1, 2])

                                with col1:
                                    st.image("https://img.icons8.com/fluency/96/future.png", width=80) # 未来っぽいアイコン
                                    st.metric(label="想定年収 (2035)", value=card_data['estimated_salary'])

                                with col2:
                                    st.subheader(card_data['job_title'])
                                    st.write(f"**Mission:** {card_data['mission']}")
                                    st.write("**Required Skills:**")
                                    # スキルをタグ風に表示
                                    st.write(" ".join([f"`{skill}`" for skill in card_data['required_skills']]))
                            else:
                                st.error("未来の予測に失敗しました。もう一度試してください。")
        else:
            st.error("質問を入力してください。")

elif app_mode == "📚 データカタログ一覧":
    st.title("📚 Data Catalog")
    st.markdown("現在データベースに格納されている全技術レポートの一覧です。")
    
    # データ取得
    df = get_all_data_as_df()
    
    # フィルタリング (サイドバーの選択に連動)
    df_filtered = df[df['Category'].isin(selected_categories)]
    
    st.info(f"全データ数: {len(df)} 件 / 表示中: {len(df_filtered)} 件")
    
    # データフレーム表示 (検索・ソート可能)
    st.dataframe(
        df_filtered,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Title": st.column_config.TextColumn("レポートタイトル", width="medium"),
            "Category": st.column_config.TextColumn("カテゴリ", width="small"),
        }
    )

# --- ログアウトボタン ---
st.sidebar.markdown("---")
if st.sidebar.button("ログアウト", key='logout_button_sidebar'):
    st.session_state["password_correct"] = False
    st.rerun()
