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

# --- 新機能: 未来日記生成ロジック ---
def generate_future_diary(topic):
    client = anthropic.Anthropic(api_key=st.secrets["CLAUDE_API_KEY"])
    
    prompt = f"""
    You are a novelist writing a 'slice of life' diary entry set in the year 2035.
    The theme is: '{topic}' is now a normal part of everyday life in Japan.
    Write a short, emotional, or funny diary entry (about 300 Japanese characters) from the perspective of an ordinary person (a student, a parent, or a worker).
    Focus on how this technology has changed feelings, scenery, or daily routine.
    
    Output format (JSON):
    {{
        "date": "2035年X月X日 (Weather)",
        "title": "Catchy Title",
        "author_profile": "Example: '14歳 中学生' or '45歳 主婦'",
        "content": "Diary content..."
    }}
    Only output the JSON.
    """
    
    try:
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )
        import json
        content = response.content[0].text
        json_str = content[content.find("{"):content.rfind("}")+1]
        return json.loads(json_str)
    except Exception as e:
        return None

# --- 新機能: 思考の深掘り（展開）ロジック ---
def generate_thought_expansion(topic, mode):
    client = anthropic.Anthropic(api_key=st.secrets["CLAUDE_API_KEY"])

    # モードに応じたプロンプトの切り替え
    if mode == "abstract":
        instruction = "Identify the superordinate concepts, macro trends, and 'Why it matters' for this technology."
        json_structure = '{"title": "Upper Concepts & Trends", "items": ["Concept 1", "Concept 2", "Why it matters"]}'
    elif mode == "concrete":
        instruction = "List specific applications, products, or industries where this technology is applied in 2030."
        json_structure = '{"title": "Specific Applications (2030)", "items": ["App 1", "App 2", "App 3"]}'
    elif mode == "analogous":
        instruction = "Suggest unexpected combinations with other fields, or analogous technologies. Cross-industry innovation ideas."
        json_structure = '{"title": "Cross-Pollination Ideas", "items": ["Idea 1", "Idea 2", "Idea 3"]}'

    prompt = f"""
    You are a technology strategist. Analyze the topic: '{topic}'.
    {instruction}

    Output format (JSON):
    {json_structure}

    Ensure the content is in Japanese, but the JSON keys remain in English. Only output the JSON.
    """

    try:
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )
        import json
        content = response.content[0].text
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

# ソースフィルター設定
CATEGORY_MAPPING = {
    "Gartner Hype Cycle 2025": "gartner_2025",
    "日経BP 技術トレンド": "nikkei_bp_2025_2035"
}

st.sidebar.markdown("---")
st.sidebar.subheader("🔍 検索対象ソース")
selected_labels = st.sidebar.multiselect(
    "分析対象を選択",
    options=list(CATEGORY_MAPPING.keys()),
    default=list(CATEGORY_MAPPING.keys())
)
selected_categories = [CATEGORY_MAPPING[label] for label in selected_labels]


# --- 画面分岐 ---

if app_mode == "💬 AIチャット (RAG)":
    st.title("🧬 NEXT-GEN CAREER BRAIN")
    st.markdown("#### **Generate Your Future Roadmap. Your Personal Growth Strategy AI.**")
    st.markdown("---")
    st.markdown("##### **[ACCESS GRANTED]**。KNOWLEDGE SYSTEM READY FOR QUERY.")
    st.markdown("---")

    # 🚨 修正ポイント1: セッションステートの初期化
    if "rag_result" not in st.session_state:
        st.session_state.rag_result = None
    if "last_query" not in st.session_state:
        st.session_state.last_query = ""

    query = st.text_area("Enter Your Question ...🤣日本語でええよ🤣", height=100)

    # 検索ボタンが押されたら、結果をセッションに保存
    if st.button("🔍 Research Techs ", type="primary", key='rag_search_button'):
        if not selected_categories:
            st.error("⚠️ 検索対象ソースが選択されていません。サイドバーで選択してください。")
        elif query:
            with st.spinner("Analyzing 700 Data Feeds... Standby for Analysis."):
                # 検索実行
                result = run_rag_search(query, selected_categories)
                # 結果とクエリを保存（これでボタンがリセットされても消えない）
                st.session_state.rag_result = result
                st.session_state.last_query = query
        else:
            st.error("質問を入力してください。")

    # 🚨 修正ポイント2: 保存された結果があれば表示（検索ボタンの外に出す）
    # 🚨 修正箇所: 結果表示ブロック全体を置き換え
    if st.session_state.rag_result:
        result = st.session_state.rag_result
        
        if isinstance(result, str):
            st.error(result)
        else:
            st.markdown(f"**💡 回答**\n\n{result['answer']}")
            st.markdown("---")
            st.markdown(f"**📚 参照された資料:** {', '.join(result['sources'])}") 
            
            with st.expander("📄 参照された原文コンテンツを確認する"):
                st.code(result['context'], language="markdown")
            # === 思考の深掘り機能エリア ===
            st.markdown("---")
            st.subheader("💡 Deep Dive & Expansion")
            st.markdown("視点を変えて、この技術を深掘りします。")
            
            # ステート初期化
            if "thought_expansion" not in st.session_state:
                st.session_state.thought_expansion = None
            
            # 3つのボタンを横並びに
            col_d1, col_d2, col_d3 = st.columns(3)
            
            with col_d1:
                if st.button("⬆️ 抽象化 (上位概念)", key="btn_abstract", use_container_width=True):
                    with st.spinner("Thinking Macro..."):
                        st.session_state.thought_expansion = generate_thought_expansion(st.session_state.last_query, "abstract")
            
            with col_d2:
                if st.button("⬇️ 具体化 (応用例)", key="btn_concrete", use_container_width=True):
                    with st.spinner("Thinking Micro..."):
                        st.session_state.thought_expansion = generate_thought_expansion(st.session_state.last_query, "concrete")
            
            with col_d3:
                if st.button("↔️ 横展開 (関連技術)", key="btn_analogous", use_container_width=True):
                    with st.spinner("Connecting Dots..."):
                        st.session_state.thought_expansion = generate_thought_expansion(st.session_state.last_query, "analogous")

            # 深掘り結果の表示
            if st.session_state.thought_expansion:
                data = st.session_state.thought_expansion
                st.info(f"**{data.get('title', 'Analysis Result')}**")
                for item in data.get('items', []):
                    st.write(f"• {item}")

            # === エンタメ機能エリア ===
            st.markdown("---")
            st.subheader("🚀 2035 Vision Simulation")
            st.markdown("この技術が実現した未来をシミュレーションします。")

            # ステート初期化（ボタンを押した結果を保持するため）
            if "career_card" not in st.session_state:
                st.session_state.career_card = None
            if "future_diary" not in st.session_state:
                st.session_state.future_diary = None

            # ボタンを2列に配置
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("🃏 未来の名刺を作る", key="btn_card", use_container_width=True):
                    with st.spinner("Designing Future Career..."):
                        st.session_state.career_card = generate_future_career(st.session_state.last_query)
                        st.session_state.future_diary = None # 片方だけ表示するようにリセット

            with col2:
                if st.button("📖 未来の日記を読む", key="btn_diary", use_container_width=True):
                    with st.spinner("Writing Future Story..."):
                        st.session_state.future_diary = generate_future_diary(st.session_state.last_query)
                        st.session_state.career_card = None # 片方だけ表示するようにリセット

            # --- 名刺の表示 ---
            if st.session_state.career_card:
                card = st.session_state.career_card
                st.success("✅ 2035年のキャリア予測")
                
                # カード風デザイン
                with st.container(border=True):
                    c1, c2 = st.columns([1, 3])
                    with c1:
                        st.image("https://img.icons8.com/fluency/96/future.png", width=70)
                    with c2:
                        st.markdown(f"### {card.get('job_title', 'Future Job')}")
                        st.caption(f"想定年収: {card.get('estimated_salary', '---')}")
                    
                    st.markdown(f"**Mission:** {card.get('mission', '')}")
                    st.markdown("**Required Skills:**")
                    st.write(" ".join([f"`{s}`" for s in card.get('required_skills', [])]))

            # --- 日記の表示 ---
            if st.session_state.future_diary:
                diary = st.session_state.future_diary
                st.info("✅ 2035年の日常ログ")
                
                # 日記風デザイン
                with st.container(border=True):
                    st.markdown(f"### 📖 {diary.get('title', '無題')}")
                    st.caption(f"📅 {diary.get('date', '2035')} | ✍️ {diary.get('author_profile', '匿名')}")
                    st.write(diary.get('content', ''))


elif app_mode == "📚 データカタログ一覧":
    st.title("📚 Data Catalog")
    # ... (カタログ表示ロジックはそのまま) ...
    # もし以前のコードからコピペが必要なら指示ください
    st.markdown("現在データベースに格納されている全技術レポートの一覧です。")
    df = get_all_data_as_df()
    df_filtered = df[df['Category'].isin(selected_categories)]
    st.info(f"全データ数: {len(df)} 件 / 表示中: {len(df_filtered)} 件")
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
    st.session_state.rag_result = None # ログアウト時に結果もクリア
    st.rerun()
