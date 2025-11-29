import streamlit as st
import os 
import json
import firebase_admin
from firebase_admin import credentials, firestore
from sentence_transformers import SentenceTransformer
import anthropic
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# --- 1. Firestore接続のためのユーティリティ関数 ---
@st.cache_resource
def setup_firestore():
    if not firebase_admin._apps:
        try:
            cert_json_string = st.secrets["firebase"]["cert_json"] 
            cert_dict = json.loads(cert_json_string) 
            cred = credentials.Certificate(cert_dict)
            firebase_admin.initialize_app(cred)
        except Exception as e:
            st.error(f"Firestore接続エラー: {e}")
            return None
    return firestore.client()

# --- 2. RAG検索ロジック ---
@st.cache_resource
def load_embedding_model():
    return SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

def run_rag_search(query, selected_categories):
    db = setup_firestore()
    if not db: return "データベース接続に失敗しました。"
    
    model = load_embedding_model()
    
    try:
        query_embedding = model.encode(query)
        
        all_docs = []
        # tech_docsコレクションからデータを取得
        docs_stream = db.collection("tech_docs").stream()
        
        for doc in docs_stream:
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

# --- 生成AI共通関数 (JSONパース強化版) ---
def call_claude_json(prompt):
    client = anthropic.Anthropic(api_key=st.secrets["CLAUDE_API_KEY"])
    try:
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )
        content = response.content[0].text
        # JSON部分抽出
        s_idx = content.find("{")
        e_idx = content.rfind("}")
        if s_idx != -1 and e_idx != -1:
            json_str = content[s_idx:e_idx+1]
            return json.loads(json_str, strict=False)
        else:
            return None
    except Exception as e:
        st.error(f"AI生成エラー: {e}")
        return None

# --- 新機能: 未来の名刺 ---
def generate_future_career(topic):
    prompt = f"""
    You are a visionary career consultant in the year 2035.
    Based on the technology topic: '{topic}', create a fictional, futuristic job profile.
    Output format (JSON):
    {{
        "job_title": "Cool sounding job title (English & Japanese)",
        "estimated_salary": "Annual salary in 2035 (JPY)",
        "required_skills": ["Skill 1", "Skill 2", "Skill 3"],
        "mission": "A short, inspiring mission statement."
    }}
    Only output the JSON.
    """
    return call_claude_json(prompt)

# --- 新機能: 未来日記 ---
def generate_future_diary(topic):
    prompt = f"""
    You are a novelist writing a 'slice of life' diary entry set in the year 2035.
    The theme is: '{topic}' is now a normal part of everyday life in Japan.
    Output format (JSON):
    {{
        "date": "2035年X月X日 (Weather)",
        "title": "Catchy Title",
        "author_profile": "Example: '14歳 中学生' or '45歳 主婦'",
        "content": "Diary content (about 300 Japanese characters)..."
    }}
    Only output the JSON.
    """
    return call_claude_json(prompt)

# --- 新機能: 思考の深掘り ---
def generate_thought_expansion(topic, mode):
    instructions = {
        "abstract": "Identify superordinate concepts, macro trends, and 'Why it matters'.",
        "concrete": "List specific applications, products, or industries in 2030.",
        "analogous": "Suggest unexpected combinations or analogous technologies."
    }
    titles = {
        "abstract": "Upper Concepts & Trends",
        "concrete": "Specific Applications (2030)",
        "analogous": "Cross-Pollination Ideas"
    }
    
    prompt = f"""
    You are a technology strategist. Analyze: '{topic}'.
    {instructions.get(mode, "")}
    Output format (JSON):
    {{
        "title": "{titles.get(mode, 'Analysis')}",
        "items": ["Item 1", "Item 2", "Item 3", "Item 4", "Item 5"]
    }}
    Ensure content is in Japanese. Only output the JSON.
    """
    return call_claude_json(prompt)

# --- 新機能: 技術階層マップ ---
def generate_tech_hierarchy(topic):
    client = anthropic.Anthropic(api_key=st.secrets["CLAUDE_API_KEY"])
    prompt = f"""
    You are a technology taxonomist. Create a hierarchical map for: '{topic}'.
    Output ONLY valid Graphviz DOT code.
    - Use 'digraph G'
    - Use rectangular nodes.
    - No markdown backticks.
    - Labels in Japanese.
    """
    try:
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )
        dot_code = response.content[0].text
        return dot_code.replace("```graphviz", "").replace("```", "").strip()
    except:
        return None

# --- 3. データ全件取得関数 ---
@st.cache_data(ttl=600)
def get_all_data_as_df():
    db = setup_firestore()
    if not db: return pd.DataFrame()
    
    docs_list = []
    for doc in db.collection("tech_docs").stream():
        d = doc.to_dict()
        docs_list.append({
            "Title": d.get('title', ''),
            "Category": d.get('category', '')
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

# --- 5. メインアプリ画面 ---

st.sidebar.title("🔧 Control Panel")
app_mode = st.sidebar.radio("モード選択", ["💬 AIチャット (RAG)", "📚 データカタログ一覧"])

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

if app_mode == "💬 AIチャット (RAG)":
    st.title("🧬 NEXT-GEN CAREER BRAIN")
    st.markdown("#### **Generate Your Future Roadmap. Your Personal Growth Strategy AI.**")
    st.markdown("---")
    st.markdown("##### **[ACCESS GRANTED]** KNOWLEDGE SYSTEM READY FOR QUERY.")
    
    # --- システムフロー図 (修正版) ---
    with st.expander("🔌 System Architecture (View Flow)"):
        st.graphviz_chart("""
        digraph RAG {
            rankdir=LR;
            node [shape=box, style=filled, fillcolor="#f9f9f9", fontname="Helvetica", fontsize=10];
            edge [fontname="Helvetica", fontsize=8];
    
            User [label="👨‍💻 USER\n(Query)", shape=ellipse, fillcolor="#e8f0fe"];
            DB [label="📚 VECTOR DB\n(700 Tech Reports)", color="blue"];
            AI [label="🧠 GENERATIVE AI\n(Claude 3 Haiku)", color="red", shape=component];
            Output [label="🚀 OUTPUT\n(Future Roadmap)", shape=note, fillcolor="#d4edda"];
    
            User -> DB [label="Semantic Search"];
            DB -> AI [label="Retrieval"];
            User -> AI [label="Context"];
            AI -> Output [label="Generation"];
            
            # 拡張機能フロー
            subgraph cluster_ext {
                label = "Expansion Features";
                style=dashed;
                Expand [label="💡 Deep Dive\n(Abstract/Concrete)", color="orange"];
                Map [label="🕸️ Tech Map", color="green"];
                Fun [label="🔮 Entertainment\n(Card/Diary)", color="purple"];
                
                Output -> Expand [style=dotted];
                Output -> Map [style=dotted];
                Output -> Fun [style=dotted];
            }
        }
        """)
    st.markdown("---")

    # ステート初期化
    if "rag_result" not in st.session_state: st.session_state.rag_result = None
    if "last_query" not in st.session_state: st.session_state.last_query = ""
    if "thought_expansion" not in st.session_state: st.session_state.thought_expansion = None
    if "career_card" not in st.session_state: st.session_state.career_card = None
    if "future_diary" not in st.session_state: st.session_state.future_diary = None

    query = st.text_area("Enter Your Question ...🤣日本語でええよ🤣", height=100)

    if st.button("🔍 Research Techs ", type="primary", key='rag_search_button'):
        if not selected_categories:
            st.error("⚠️ 検索対象ソースが選択されていません。")
        elif query:
            # 検索時は他の結果をリセット
            st.session_state.thought_expansion = None
            st.session_state.career_card = None
            st.session_state.future_diary = None
            
            with st.spinner("Analyzing 700 Data Feeds... Standby for Analysis."):
                result = run_rag_search(query, selected_categories)
                st.session_state.rag_result = result
                st.session_state.last_query = query
        else:
            st.error("質問を入力してください。")

    # --- 結果表示エリア ---
    if st.session_state.rag_result:
        result = st.session_state.rag_result
        
        if isinstance(result, str):
            st.error(result)
        else:
            # RAG回答
            st.markdown(f"**💡 回答**\n\n{result['answer']}")
            st.markdown("---")
            st.markdown(f"**📚 参照された資料:** {', '.join(result['sources'])}") 
            
            with st.expander("📄 参照された原文コンテンツを確認する"):
                st.code(result['context'], language="markdown")

            # === 思考の深掘り機能エリア ===
            st.markdown("---")
            st.subheader("💡 Deep Dive & Expansion")
            
            c_d1, c_d2, c_d3 = st.columns(3)
            with c_d1:
                if st.button("⬆️ 抽象化 (上位概念)", key="btn_abstract", use_container_width=True):
                    with st.spinner("Thinking Macro..."):
                        st.session_state.thought_expansion = generate_thought_expansion(st.session_state.last_query, "abstract")
            with c_d2:
                if st.button("⬇️ 具体化 (応用例)", key="btn_concrete", use_container_width=True):
                    with st.spinner("Thinking Micro..."):
                        st.session_state.thought_expansion = generate_thought_expansion(st.session_state.last_query, "concrete")
            with c_d3:
                if st.button("↔️ 横展開 (関連技術)", key="btn_analogous", use_container_width=True):
                    with st.spinner("Connecting Dots..."):
                        st.session_state.thought_expansion = generate_thought_expansion(st.session_state.last_query, "analogous")

            if st.session_state.thought_expansion:
                data = st.session_state.thought_expansion
                st.markdown(f"#### {data.get('title', 'Analysis')}")
                st.caption("※ AIによるアイデア展開です。")
                for item in data.get('items', []):
                    st.write(f"• {item}")

            # === 技術マップ ===
            st.markdown("")
            if st.button("🕸️ 技術体系マップを表示する", key="btn_map", use_container_width=True):
                with st.spinner("Mapping..."):
                    dot = generate_tech_hierarchy(st.session_state.last_query)
                    if dot:
                        st.graphviz_chart(dot)
                        st.caption("※ AI生成の概念図")

            # === エンタメ機能エリア ===
            st.markdown("---")
            st.subheader("🚀 2035 Vision Simulation")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🃏 未来の名刺を作る", key="btn_card", use_container_width=True):
                    with st.spinner("Designing..."):
                        st.session_state.career_card = generate_future_career(st.session_state.last_query)
                        st.session_state.future_diary = None
            with col2:
                if st.button("📖 未来の日記を読む", key="btn_diary", use_container_width=True):
                    with st.spinner("Writing..."):
                        st.session_state.future_diary = generate_future_diary(st.session_state.last_query)
                        st.session_state.career_card = None

            if st.session_state.career_card:
                card = st.session_state.career_card
                st.success("✅ 2035 Career Prediction")
                with st.container(border=True):
                    c1, c2 = st.columns([1, 3])
                    with c1: st.image("https://img.icons8.com/fluency/96/future.png", width=70)
                    with c2:
                        st.markdown(f"### {card.get('job_title', 'Future Job')}")
                        st.caption(f"推定年収: {card.get('estimated_salary', '---')}")
                    st.write(f"**Mission:** {card.get('mission', '')}")
                    st.write(f"**Skills:** {', '.join(card.get('required_skills', []))}")

            if st.session_state.future_diary:
                diary = st.session_state.future_diary
                st.info("✅ 2035 Daily Log")
                with st.container(border=True):
                    st.markdown(f"### 📖 {diary.get('title', 'Diary')}")
                    st.caption(f"📅 {diary.get('date', '')} | ✍️ {diary.get('author_profile', '')}")
                    st.write(diary.get('content', ''))

elif app_mode == "📚 データカタログ一覧":
    st.title("📚 Data Catalog")
    st.markdown("現在データベースに格納されている全技術レポートの一覧です。")
    df = get_all_data_as_df()
    if not df.empty:
        df_filtered = df[df['Category'].isin(selected_categories)]
        st.info(f"全データ数: {len(df)} 件 / 表示中: {len(df_filtered)} 件")
        st.dataframe(df_filtered, use_container_width=True, hide_index=True)
    else:
        st.warning("データが見つかりません。")

# --- ログアウト ---
st.sidebar.markdown("---")
if st.sidebar.button("ログアウト", key='logout_button_sidebar'):
    st.session_state["password_correct"] = False
    st.session_state.rag_result = None
    st.rerun()
