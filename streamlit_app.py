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
import base64 # 👈 画像表示用に必要

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
    if not db: return {"answer": "DB接続失敗", "sources": [], "context": "", "meta_context": ""}
    
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
            return {"answer": "データが見つかりません。", "sources": [], "context": "", "meta_context": ""}

        doc_embeddings = np.array([doc['embedding'] for doc in all_docs])
        similarities = cosine_similarity(query_embedding.reshape(1, -1), doc_embeddings).flatten()
        
        top_indices = np.argsort(similarities)[::-1][:5]
        top_docs = [all_docs[i] for i in top_indices]

        context_text = "\n\n---\n\n".join([doc.get('content', '') for doc in top_docs])
        
        # 思考エレベーター用のメタデータ抽出
        meta_context_list = []
        for doc in top_docs:
            title = doc.get('title', 'No Title')
            summary = doc.get('summary_section', '')
            analysis = doc.get('analysis_section', '')
            meta_context_list.append(f"■事例名: {title}\n[要約]\n{summary}\n[分析]\n{analysis}")
        meta_context = "\n\n".join(meta_context_list)
        
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
            model="claude-3-haiku-20240307", # 👈 Haikuに統一
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        sources = [doc.get('title', '不明') for doc in top_docs]
        
        return {
            "answer": response.content[0].text,
            "sources": sources,
            "context": context_text,
            "meta_context": meta_context
        }
            
    except Exception as e:
        return {"answer": f"エラー: {e}", "sources": [], "context": "", "meta_context": ""}

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

# --- Mermaid図の描画関数 (画像変換版: 最も安定) ---
def render_mermaid(graph_code):
    graphbytes = graph_code.encode("utf8")
    base64_bytes = base64.urlsafe_b64encode(graphbytes)
    base64_string = base64_bytes.decode("ascii")
    url = f"https://mermaid.ink/img/{base64_string}"
    st.image(url, use_container_width=True)

# --- 新機能群 ---
def generate_future_career(topic):
    prompt = f"""
    あなたは2035年のキャリアコンサルタントです。
    トピック: '{topic}' に基づいて、未来的でかっこいい架空の職業プロフィールを作成してください。
    【重要】日本語で出力してください。
    Output format (JSON):
    {{
        "job_title": "英語名 / 日本語名",
        "estimated_salary": "15,000,000 JPY",
        "required_skills": ["スキル1", "スキル2", "スキル3"],
        "mission": "短く、情熱的なミッションステートメント"
    }}
    Only output the JSON.
    """
    return call_claude_json(prompt)

def generate_future_diary(topic):
    prompt = f"""
    あなたは小説家です。2035年を舞台に、'{topic}' が日常になった世界のショートショート日記を書いてください。
    【重要】日本語で出力してください。
    Output format (JSON):
    {{
        "date": "2035年X月X日 (天気)",
        "title": "タイトル",
        "author_profile": "例: 14歳 中学生",
        "content": "日記の本文..."
    }}
    Only output the JSON.
    """
    return call_claude_json(prompt)

def generate_thought_expansion(topic, mode, meta_context=""):
    base_inst = f"参照データ:\n{meta_context}" if meta_context else ""
    instructions = {
        "abstract": "この技術の上位概念、マクロトレンド、なぜ重要かを分析してください。",
        "concrete": "2030年における具体的な応用例、製品、産業をリストアップしてください。",
        "analogous": "意外な組み合わせ、他分野への転用、アナロジーを提案してください。"
    }
    titles = {
        "abstract": "抽象化 (上位概念・トレンド)",
        "concrete": "具体化 (2030年の応用例)",
        "analogous": "横展開 (異分野結合)"
    }
    
    prompt = f"""
    あなたは技術ストラテジストです。トピック: '{topic}' を分析してください。
    {base_inst}
    指示: {instructions.get(mode, "")}
    【重要】日本語で出力してください。
    Output format (JSON):
    {{
        "title": "{titles.get(mode, '分析結果')}",
        "items": ["項目1", "項目2", "項目3", "項目4", "項目5"]
    }}
    Only output the JSON.
    """
    return call_claude_json(prompt)

def generate_tech_hierarchy(topic):
    client = anthropic.Anthropic(api_key=st.secrets["CLAUDE_API_KEY"])
    prompt = f"""
    Create a hierarchical technology map for: '{topic}'.
    IMPORTANT: Extract main keywords. Labels MUST be in Japanese.
    Output ONLY valid Graphviz DOT code.
    - Use 'digraph G'
    - Use rectangular nodes.
    - No markdown backticks.
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

# --- 4. 認証ロジック ---
def check_password():
    input_pass = st.session_state.get("password_input")
    authorized_users = st.secrets.get("user_passwords", {})
    for username, password in authorized_users.items():
        if input_pass == password:
            del st.session_state["password_input"]
            st.session_state["current_user"] = username
            return True
    if input_pass == st.secrets.get("APP_PASSWORD"):
        del st.session_state["password_input"]
        st.session_state["current_user"] = "Family Member"
        return True
    return False

if "password_correct" not in st.session_state:
    st.session_state["password_correct"] = False
if "current_user" not in st.session_state:
    st.session_state["current_user"] = "Guest"

if not st.session_state["password_correct"]:
    st.title("⚔️ CAREER DATA VAULT: AUTH")
    st.markdown("##### 次世代戦略AIへアクセスするには、認証が必要です。")
    with st.form("login_form"):
        st.text_input("パスワード", type="password", key="password_input")
        if st.form_submit_button("Login"):
            if check_password():
                st.session_state["password_correct"] = True
                st.rerun() 
            else:
                st.error('パスワードが間違っています。')
    st.stop() 

# --- 5. メインアプリ画面 ---

st.sidebar.title("🔧 Control Panel")
user_name = st.session_state.get("current_user", "Guest")
st.sidebar.caption(f"Login as: **{user_name}**")

if st.sidebar.button("ログアウト", key='logout_top'):
    st.session_state["password_correct"] = False
    st.session_state["current_user"] = None
    st.session_state.rag_result = None
    st.rerun()

app_mode = st.sidebar.radio("モード選択", ["💬 AIチャット (RAG)", "📚 データカタログ一覧"])

CATEGORY_MAPPING = {
    "Gartner Hype Cycle 2025": "gartner_2025",
    "日経BP 技術トレンド": "nikkei_bp_2025_2035",
    "次世代発電技術": "次世代発電",
    "自動車産業予測 2045": "自動車産業2045",
    "[記事] AI & Info": "AIinfo",
    "[記事] Python & Web": "python_and_webtech",
    "[記事] 品質・セキュリティ": "Quality_and_Sequrity",
    "[記事] 半導体コラム": "Semiconductor",
    "[記事] Tips": "Tips"
}

st.sidebar.markdown("---")
st.sidebar.subheader("🔍 検索対象ソース")
st.sidebar.caption("検索したいデータソースにチェックを入れてください")
selected_categories = []
for label, category_id in CATEGORY_MAPPING.items():
    if st.sidebar.checkbox(label, value=True, key=f"check_{category_id}"):
        selected_categories.append(category_id)

if app_mode == "💬 AIチャット (RAG)":
    st.title("🧬 NEXT-GEN CAREER BRAIN")
    st.image("tech-trend-rag-family.jpg", caption="Concept: The Future Career Exploring System", use_container_width=True)
    st.markdown("---")
    st.markdown("##### **[ACCESS GRANTED]** KNOWLEDGE SYSTEM READY FOR QUERY.")
    
    # 🔌 システムフロー図 (Mermaid画像版: 修正済み)
    st.markdown("#### 🔌 System Architecture")
    render_mermaid("""
    graph LR
        %% ノード定義
        User(("👨‍💻 USER<br>(Query)"))
        DB[("📚 VECTOR DB<br>(700 Reports)")]
        AI[["🧠 GEN-AI<br>(Claude 3 Haiku)"]]
        Output> "🚀 OUTPUT<br>(RAG Result)"]

        %% フロー定義
        User -->|"Semantic Search"| DB
        DB -->|"Retrieval"| AI
        User -->|"Context"| AI
        AI -->|"Generation"| Output

        %% 拡張機能エリア（並列処理を表現）
        subgraph Ext [Expansion Features (Direct API Call)]
            direction TB
            DeepDive("💡 Deep Dive<br>(Analysis)")
            Map("🕸️ Tech Map<br>(Visualization)")
            Fun("🔮 2035 Vision<br>(Card/Diary)")
        end
        
        %% AIから拡張機能への点線接続
        AI -.->|"Analyze"| DeepDive
        AI -.->|"Visualize"| Map
        AI -.->|"Imagine"| Fun

        %% スタイル定義
        style User fill:#e8f0fe,stroke:#333,stroke-width:2px
        style DB fill:#e6f3ff,stroke:#00f,stroke-width:2px
        style AI fill:#ffebee,stroke:#f00,stroke-width:2px
        style Output fill:#d4edda,stroke:#333,stroke-width:2px
        style Ext fill:#fff,stroke:#999,stroke-dasharray: 5 5
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
            st.session_state.thought_expansion = None
            st.session_state.career_card = None
            st.session_state.future_diary = None
            with st.spinner("Analyzing 700 Data Feeds... Standby for Analysis."):
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
            with st.expander("📄 参照データ（原文・抽出メタデータ）を確認する"):
                st.caption("▼ RAGで使用された原文")
                st.code(result['context'], language="markdown")
                if result.get('meta_context'):
                    st.caption("▼ 思考エレベーター用抽出データ（要約・分析）")
                    st.code(result['meta_context'], language="markdown")
            
            # === 思考の深掘り ===
            st.markdown("---")
            st.subheader("💡 Deep Dive & Expansion")
            c1, c2, c3 = st.columns(3)
            
            # メタデータの取得（エラー回避用）
            meta_context = result.get('meta_context', '')
            
            with c1: 
                if st.button("⬆️ 抽象化", key="btn_abs", use_container_width=True):
                    with st.spinner("Thinking Macro..."):
                        st.session_state.thought_expansion = generate_thought_expansion(
                            st.session_state.last_query, "abstract", meta_context)
            with c2: 
                if st.button("⬇️ 具体化", key="btn_con", use_container_width=True):
                    with st.spinner("Thinking Micro..."):
                        st.session_state.thought_expansion = generate_thought_expansion(
                            st.session_state.last_query, "concrete", meta_context)
            with c3: 
                if st.button("↔️ 横展開", key="btn_ana", use_container_width=True):
                    with st.spinner("Connecting Dots..."):
                        st.session_state.thought_expansion = generate_thought_expansion(
                            st.session_state.last_query, "analogous", meta_context)

            if st.session_state.thought_expansion:
                d = st.session_state.thought_expansion
                st.markdown(f"#### {d.get('title', 'Analysis')}")
                st.caption("※ 検索された技術資料の「要約・分析」情報をベースに、AIが洞察を広げました。")
                for item in d.get('items', []): st.write(f"• {item}")

            # === 技術マップ ===
            st.markdown("")
            if st.button("🕸️ 技術体系マップを表示する", key="btn_map", use_container_width=True):
                with st.spinner("Mapping..."):
                    dot = generate_tech_hierarchy(st.session_state.last_query)
                    if dot:
                        st.success("✅ マップ生成完了")
                        st.graphviz_chart(dot)
                        st.caption("※ AI生成の概念図")
                    else:
                        st.error("マップ生成に失敗しました")

            # === エンタメ機能 ===
            st.markdown("---")
            st.subheader("🚀 2035 Vision Simulation")
            ec1, ec2 = st.columns(2)
            with ec1:
                if st.button("🃏 未来の名刺", key="btn_card", use_container_width=True):
                    with st.spinner("Designing..."):
                        st.session_state.career_card = generate_future_career(st.session_state.last_query)
                        st.session_state.future_diary = None
            with ec2:
                if st.button("📖 未来の日記", key="btn_diary", use_container_width=True):
                    with st.spinner("Writing..."):
                        st.session_state.future_diary = generate_future_diary(st.session_state.last_query)
                        st.session_state.career_card = None

            if st.session_state.career_card:
                c = st.session_state.career_card
                st.success("✅ 2035 Career Prediction")
                with st.container(border=True):
                    col_img, col_txt = st.columns([1, 3])
                    with col_img: st.image("https://img.icons8.com/fluency/96/future.png", width=80)
                    with col_txt:
                        st.markdown(f"### {c.get('job_title', 'Unknown Job')}")
                        st.metric(label="想定年収 (2035)", value=c.get('estimated_salary', '---'))
                    st.write(f"**Mission:** {c.get('mission', '')}")
                    st.write(f"**Skills:** {', '.join(c.get('required_skills', []))}")

            if st.session_state.future_diary:
                d = st.session_state.future_diary
                st.info("✅ 2035 Daily Log")
                with st.container(border=True):
                    st.markdown(f"### 📖 {d.get('title', 'Diary')}")
                    st.caption(f"📅 {d.get('date', '')} | ✍️ {d.get('author_profile', '')}")
                    st.write(d.get('content', ''))
        else:
            st.error(result)

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

st.sidebar.markdown("---")
