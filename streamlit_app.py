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

def generate_thought_expansion(topic, mode):
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

# --- 3. データ全件取得関数 ---
@st.cache_data(ttl=600)
def get_all_data_as_df():
    db = setup_firestore()
    if not db: return pd.DataFrame()
    docs_list = []
    for doc in db.collection("tech_docs").stream():
        d = doc.to_dict()
        docs_list.append({"Title": d.get('title', ''), "Category": d.get('category', '')})
    return pd.DataFrame(docs_list)

# --- 4. 認証ロジック (マルチユーザー対応) ---
def check_password():
    """入力されたパスワードが登録済みユーザーのものか確認する"""
    input_pass = st.session_state.get("password_input")
    
    # Secretsからユーザー辞書を取得 (なければ旧APP_PASSWORDで救済)
    authorized_users = st.secrets.get("user_passwords", {})
    
    # マルチユーザーチェック
    for username, password in authorized_users.items():
        if input_pass == password:
            del st.session_state["password_input"]
            st.session_state["current_user"] = username # ユーザー名を保存
            return True
            
    # 旧設定へのフォールバック
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

# 🚨 修正箇所: ログアウトボタンをここに移動
# ログイン中のユーザー名を表示
current_user = st.session_state.get("current_user", "Guest")
st.sidebar.caption(f"Login as: **{current_user}**")

if st.sidebar.button("ログアウト", key='logout_top'):
    # ログアウト処理
    st.session_state["password_correct"] = False
    st.session_state["current_user"] = None
    st.session_state.rag_result = None
    st.session_state.thought_expansion = None
    st.session_state.career_card = None
    st.session_state.future_diary = None
    st.rerun()

st.sidebar.markdown("---")



app_mode = st.sidebar.radio("モード選択", ["💬 AIチャット (RAG)", "📚 データカタログ一覧"])

CATEGORY_MAPPING = {
    "Gartner Hype Cycle 2025": "gartner_2025",
    "日経BP 技術トレンド": "nikkei_bp_2025_2035",
    "次世代発電技術": "次世代発電",
    "自動車産業予測 2045": "自動車産業2045",
    "Articles: AI Info": "AIinfo",
    "Articles: Python & Web": "python_and_webtech",
    "Articles: Quality & Security": "Quality_and_Sequrity",
    "Articles: Semiconductor": "Semiconductor",
    "Articles: Tips": "Tips"
}

st.sidebar.markdown("---")
st.sidebar.subheader("🔍 検索対象ソース")
st.sidebar.caption("検索したいデータソースにチェックを入れてください")
selected_categories = []
for label, category_id in CATEGORY_MAPPING.items():
    if st.sidebar.checkbox(label, value=True, key=f"check_{category_id}"):
        selected_categories.append(category_id)

if app_mode == "💬 AIチャット (RAG)":
    
    # 🚨 Welcomeメッセージの表示
    user_name = st.session_state.get("current_user", "Guest")
    st.success(f"👋 Welcome! {user_name}")

    st.title("🧬 NEXT-GEN CAREER BRAIN")
    st.image("tech-trend-rag-family.jpg", caption="Concept: The Future Career Exploring System", use_container_width=True)
    st.markdown("---")
    st.markdown("##### **[ACCESS GRANTED]** KNOWLEDGE SYSTEM READY FOR QUERY.")

    # プロンプトガイド
    with st.expander("💡 ヒント：AIの性能を最大限に引き出す入力のコツ"):
        st.markdown("""
        **1. RAG検索（回答）の精度を上げたいとき**
        * 具体的に書く: 「AI」ではなく「化学プラントにおけるAI活用事例」
        **2. 技術マップを綺麗に出したいとき**
        * 関係性を問う: 「〇〇を実現するための技術要素を教えて」
        """)

    # システム図
    st.markdown("#### 🔌 System Architecture")
    st.graphviz_chart("""
    digraph RAG {
        rankdir=LR;
        node [shape=box, style=filled, fillcolor="#f9f9f9", fontname="sans-serif"];
        edge [fontname="sans-serif"];
        User [label="USER", shape=ellipse, fillcolor="#e8f0fe"];
        DB [label="VECTOR DB", color="blue"];
        AI [label="GEN-AI", color="red"];
        Output [label="OUTPUT", shape=note, fillcolor="#d4edda"];
        User -> DB; DB -> AI; User -> AI; AI -> Output;
        
        subgraph cluster_ext {
            label = "Expansion";
            style=dashed;
            color=gray;
            DeepDive [label="Deep Dive"];
            Map [label="Tech Map"];
            Fun [label="Entertainment"];
            Output -> DeepDive [style=dotted];
            Output -> Map [style=dotted];
            Output -> Fun [style=dotted];
        }
    }
    """, use_container_width=True)
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
                st.markdown(f"#### {d.get('title', 'Analysis')}")
                st.caption("※ AIによるアイデア展開です。")
                for item in d.get('items', []): st.write(f"• {item}")

            st.markdown("")
            if st.button("🕸️ 技術マップ", key="btn_map", use_container_width=True):
                with st.spinner("Mapping..."):
                    dot = generate_tech_hierarchy(st.session_state.last_query)
                    if dot:
                        st.success("✅ マップ生成完了")
                        st.graphviz_chart(dot)
                        st.caption("※ AI生成の概念図")

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
                st.success("✅ 2035 Career Prediction")
                with st.container(border=True):
                    col_img, col_txt = st.columns([1, 3])
                    with col_img: st.image("https://img.icons8.com/fluency/96/future.png", width=80)
                    with col_txt:
                        st.markdown(f"### {c.get('job_title', 'Future Job')}")
                        st.metric(label="想定年収 (2035)", value=c.get('estimated_salary', '---'))
                    st.write(f"**Mission:** {c.get('mission', '')}")
                    st.write(f"**Skills:** {', '.join(c.get('required_skills', []))}")

            if st.session_state.future_diary:
                d = st.session_state.future_diary
                st.info("✅ 2035 Log")
                with st.container(border=True):
                    st.markdown(f"### {d.get('title')}")
                    st.caption(f"{d.get('date')} | {d.get('author_profile')}")
                    st.write(d.get('content'))
        else:
            st.error(result)

elif app_mode == "📚 データカタログ一覧":
    st.title("📚 Data Catalog")
    df = get_all_data_as_df()
    if not df.empty:
        df_filtered = df[df['Category'].isin(selected_categories)]
        st.info(f"全データ数: {len(df)} 件 / 表示中: {len(df_filtered)} 件")
        st.dataframe(df_filtered, use_container_width=True, hide_index=True)

#st.sidebar.markdown("---")
#if st.sidebar.button("ログアウト", key='logout'):
#    st.session_state["password_correct"] = False
#    st.session_state["current_user"] = None
#    st.session_state.rag_result = None
#    st.rerun()
