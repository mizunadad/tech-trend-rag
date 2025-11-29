import streamlit as st
import os 
import json
import shutil # 診断用
import firebase_admin
from firebase_admin import credentials, firestore
from sentence_transformers import SentenceTransformer
import anthropic
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# --- 1. Firestore接続 ---
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
    if not db: return {"answer": "DB接続失敗", "sources": [], "context": ""}
    
    model = load_embedding_model()
    
    try:
        query_embedding = model.encode(query)
        
        all_docs = []
        docs_stream = db.collection("tech_docs").stream()
        
        for doc in docs_stream:
            data = doc.to_dict()
            data['doc_id'] = doc.id
            if data.get('category') in selected_categories:
                all_docs.append(data)

        if not all_docs:
            return {"answer": "データが見つかりません。", "sources": [], "context": ""}

        doc_embeddings = np.array([doc['embedding'] for doc in all_docs])
        similarities = cosine_similarity(query_embedding.reshape(1, -1), doc_embeddings).flatten()
        
        top_indices = np.argsort(similarities)[::-1][:5]
        top_docs = [all_docs[i] for i in top_indices]

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
        return {"answer": f"エラー: {e}", "sources": [], "context": ""}

# --- 生成AI共通関数 ---
def call_claude_json(prompt):
    client = anthropic.Anthropic(api_key=st.secrets["CLAUDE_API_KEY"])
    try:
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )
        content = response.content[0].text
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

# --- 新機能群 ---
def generate_future_career(topic):
    prompt = f"""
    You are a visionary career consultant in the year 2035.
    Based on the technology topic: '{topic}', create a fictional, futuristic job profile.
    Output format (JSON):
    {{
        "job_title": "Job Title (Japanese)",
        "estimated_salary": "Annual salary (JPY)",
        "required_skills": ["Skill 1", "Skill 2"],
        "mission": "Short mission statement."
    }}
    Only output the JSON.
    """
    return call_claude_json(prompt)

def generate_future_diary(topic):
    prompt = f"""
    You are a novelist. Write a short diary entry set in 2035 where '{topic}' is normal.
    Output format (JSON):
    {{
        "date": "2035/MM/DD",
        "title": "Title",
        "author_profile": "Profile",
        "content": "Diary content..."
    }}
    Only output the JSON.
    """
    return call_claude_json(prompt)

def generate_thought_expansion(topic, mode):
    instructions = {
        "abstract": "Identify superordinate concepts.",
        "concrete": "List specific applications in 2030.",
        "analogous": "Suggest unexpected combinations."
    }
    prompt = f"""
    Analyze: '{topic}'. {instructions.get(mode, "")}
    Output format (JSON): {{"title": "Title", "items": ["Item 1", "Item 2"]}}
    Only output the JSON.
    """
    return call_claude_json(prompt)

def generate_tech_hierarchy(topic):
    client = anthropic.Anthropic(api_key=st.secrets["CLAUDE_API_KEY"])
    prompt = f"""
    Create a hierarchical map for: '{topic}'.
    Output ONLY valid Graphviz DOT code.
    - Use 'digraph G'
    - Use rectangular nodes.
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

@st.cache_data(ttl=600)
def get_all_data_as_df():
    db = setup_firestore()
    if not db: return pd.DataFrame()
    docs_list = []
    for doc in db.collection("tech_docs").stream():
        d = doc.to_dict()
        docs_list.append({"Title": d.get('title', ''), "Category": d.get('category', '')})
    return pd.DataFrame(docs_list)

# --- 認証 ---
def check_password():
    if st.session_state.get("password_input") == st.secrets.get("APP_PASSWORD"):
        del st.session_state["password_input"] 
        return True
    return False

if "password_correct" not in st.session_state:
    st.session_state["password_correct"] = False

if not st.session_state["password_correct"]:
    st.title("⚔️ CAREER DATA VAULT: AUTH")
    with st.form("login_form"):
        st.text_input("パスワード", type="password", key="password_input")
        if st.form_submit_button("Login"):
            if check_password():
                st.session_state["password_correct"] = True
                st.rerun() 
            else:
                st.error('パスワードが間違っています。')
    st.stop() 

# --- メインアプリ ---
st.sidebar.title("🔧 Control Panel")
app_mode = st.sidebar.radio("モード選択", ["💬 AIチャット (RAG)", "📚 データカタログ一覧"])

CATEGORY_MAPPING = {
    "Gartner Hype Cycle 2025": "gartner_2025",
    "日経BP 技術トレンド": "nikkei_bp_2025_2035"
}

st.sidebar.markdown("---")
st.sidebar.subheader("🔍 検索対象ソース")
selected_labels = st.sidebar.multiselect("分析対象を選択", list(CATEGORY_MAPPING.keys()), list(CATEGORY_MAPPING.keys()))
selected_categories = [CATEGORY_MAPPING[label] for label in selected_labels]

if app_mode == "💬 AIチャット (RAG)":
    st.title("🧬 NEXT-GEN CAREER BRAIN")
    st.markdown("#### **Generate Your Future Roadmap. Your Personal Growth Strategy AI.**")
    st.markdown("---")
    st.markdown("##### **[ACCESS GRANTED]** KNOWLEDGE SYSTEM READY FOR QUERY.")
    st.markdown("---")

    # 🚨 修正: st.expander を削除し、タイトルと図を直接配置
    st.markdown("#### 🔌 System Architecture")
    
    # 🚨 修正: RAGと拡張機能を並列（Parallel）に描画する図に変更
    st.graphviz_chart("""
    digraph RAG {
        rankdir=LR;
        # ノードとエッジの共通設定
        node [shape=box, style=filled, fillcolor="#f9f9f9", fontname="sans-serif"];
        edge [fontname="sans-serif", fontsize=10];

        # 主要アクター
        User [label="USER\n(Query)", shape=ellipse, fillcolor="#e8f0fe"];
        DB [label="VECTOR DB\n(700 Reports)", color="blue"];
        AI [label="GEN-AI\n(Claude 3)", color="red", style="filled,rounded"];

        # 1. RAGフロー (メインの出力)
        RAG_Out [label="RAG OUTPUT\n(Fact Answer)", shape=note, fillcolor="#d4edda"];

        # 2. 拡張機能フロー (RAGとは独立した直接生成)
        subgraph cluster_expansion {
            label = "Expansion Features (Direct API Call)";
            style=dashed;
            color="#666666";
            fontcolor="#666666";
            
            DeepDive [label="💡 Deep Dive\n(Analysis/Map)", shape=component, fillcolor="#fff3cd"];
            Vision [label="🚀 2035 Vision\n(Card/Diary)", shape=component, fillcolor="#e8daef"];
        }

        # RAGの接続 (実線)
        User -> DB [label="Semantic Search"];
        DB -> AI [label="Context"];
        User -> AI [label="Query"];
        AI -> RAG_Out [label="Generation"];

        # 拡張機能の接続 (点線：DBを経由しない独立プロセス)
        AI -> DeepDive [label="Parallel Gen", style=dotted];
        AI -> Vision [label="Parallel Gen", style=dotted];
        
        # 配置の調整（出力を縦に並べて見やすく）
        {rank=same; RAG_Out; DeepDive; Vision}
    }
    """, use_container_width=True)


    st.markdown("---")
    # ステート管理
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
            st.session_state.thought_expansion = None
            st.session_state.career_card = None
            st.session_state.future_diary = None
            with st.spinner("Analyzing..."):
                st.session_state.rag_result = run_rag_search(query, selected_categories)
                st.session_state.last_query = query
        else:
            st.error("質問を入力してください。")

    if st.session_state.rag_result:
        result = st.session_state.rag_result
        if isinstance(result, dict):
            st.markdown(f"**💡 回答**\n\n{result['answer']}")
            st.markdown("---")
            sources_str = ', '.join(result['sources']) if result['sources'] else "なし"
            st.markdown(f"**📚 参照された資料:** {sources_str}") 
            with st.expander("📄 参照された原文"): st.code(result['context'], language="markdown")
            
            # 深掘りボタン
            st.markdown("---")
            st.subheader("💡 Deep Dive & Expansion")
            c1, c2, c3 = st.columns(3)
            with c1: 
                if st.button("⬆️ 抽象化", key="btn_abs", use_container_width=True):
                    st.session_state.thought_expansion = generate_thought_expansion(st.session_state.last_query, "abstract")
            with c2: 
                if st.button("⬇️ 具体化", key="btn_con", use_container_width=True):
                    st.session_state.thought_expansion = generate_thought_expansion(st.session_state.last_query, "concrete")
            with c3: 
                if st.button("↔️ 横展開", key="btn_ana", use_container_width=True):
                    st.session_state.thought_expansion = generate_thought_expansion(st.session_state.last_query, "analogous")

            if st.session_state.thought_expansion:
                d = st.session_state.thought_expansion
                st.markdown(f"#### {d.get('title')}")
                for i in d.get('items', []): st.write(f"• {i}")

            # マップ
            st.markdown("")
            if st.button("🕸️ 技術マップ", key="btn_map", use_container_width=True):
                dot = generate_tech_hierarchy(st.session_state.last_query)
                if dot: st.graphviz_chart(dot)

            # エンタメ
            st.markdown("---")
            st.subheader("🚀 2035 Vision Simulation")
            ec1, ec2 = st.columns(2)
            with ec1:
                if st.button("🃏 未来の名刺", key="btn_card", use_container_width=True):
                    st.session_state.career_card = generate_future_career(st.session_state.last_query)
                    st.session_state.future_diary = None
            with ec2:
                if st.button("📖 未来の日記", key="btn_diary", use_container_width=True):
                    st.session_state.future_diary = generate_future_diary(st.session_state.last_query)
                    st.session_state.career_card = None

            if st.session_state.career_card:
                c = st.session_state.career_card
                st.success("✅ Career Prediction")
                st.markdown(f"### {c.get('job_title')}")
                st.write(f"**Mission:** {c.get('mission')}")

            if st.session_state.future_diary:
                d = st.session_state.future_diary
                st.info("✅ 2035 Log")
                st.markdown(f"### {d.get('title')}")
                st.write(d.get('content'))
        else:
            st.error(result)

elif app_mode == "📚 データカタログ一覧":
    st.title("📚 Data Catalog")
    df = get_all_data_as_df()
    if not df.empty:
        df_filtered = df[df['Category'].isin(selected_categories)]
        st.dataframe(df_filtered, use_container_width=True, hide_index=True)

st.sidebar.markdown("---")
if st.sidebar.button("ログアウト", key='logout'):
    st.session_state["password_correct"] = False
    st.session_state.rag_result = None
    st.rerun()
