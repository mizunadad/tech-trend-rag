
import os
import re
import datetime
from pathlib import Path
from sentence_transformers import SentenceTransformer
import firebase_admin
from firebase_admin import credentials, firestore
import frontmatter

# --- 初期化処理 ---

if not firebase_admin._apps:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

print("Embeddingモデルをロード中...")
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

def extract_section(content, keywords):
    """
    指定されたキーワードを含む見出し(H2)のセクション内容を抽出する
    H3(###)以下の見出しはセクションの一部として含める
    """
    kw_pattern = "|".join([re.escape(k) for k in keywords])

    # 🚨 修正箇所:
    # 1. 開始: ^##\s+ (レベル2見出しに限定)
    # 2. 終了: (?=^#{1,2}\s|\Z) (レベル1かレベル2の見出しが来るまで読み込む)
    #    これにより、### (レベル3) は本文として扱われる
    regex = re.compile(rf"^##\s+.*?({kw_pattern}).*?$\s+(.*?)(?=^#{{1,2}}\s|\Z)", re.MULTILINE | re.DOTALL)

    match = regex.search(content)
    if match:
        return match.group(2).strip()
    return ""

def clean_yaml(content):
    """YAMLヘッダーの修復"""
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return content

    yaml_block = match.group(1)
    lines = yaml_block.split('\n')
    fixed_lines = []

    for line in lines:
        if re.match(r"^[a-zA-Z0-9_-]+:[^ \n]", line):
            line = re.sub(r"^([a-zA-Z0-9_-]+):", r"\1: ", line)
        fixed_lines.append(line)

    corrected_yaml = '\n'.join(fixed_lines)
    return content.replace(yaml_block, corrected_yaml)

def process_md_files():
    md_dirs = [
        "./gartner_2025",
        "./nikkei_bp_2025_2035",
        "./次世代発電",
        "./自動車産業2045",
        "./Articles_2025"
    ]

    print("--- データ登録開始 (構造化モード・階層対応版) ---")

    for md_dir_path in md_dirs:
        base_dir = Path(md_dir_path)
        if not base_dir.exists(): continue

        for md_file in base_dir.rglob("*.md"):
            if ".git" in str(md_file) or ".firebase" in str(md_file) or "venv" in str(md_file): continue

            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    raw_content = f.read()

                cleaned_content = clean_yaml(raw_content)
                post = frontmatter.loads(cleaned_content)
                metadata = post.metadata
                content_body = post.content

                date_val = metadata.get('date')
                if date_val:
                    if isinstance(date_val, datetime.date) and not isinstance(date_val, datetime.datetime):
                        date_val = datetime.datetime.combine(date_val, datetime.time.min)

                # セクション抽出 (キーワードは維持)
                summary_section = extract_section(content_body, [
                    "全体要約", "技術動向", "技術要約", "Summary", "要点", "サマリー", "summary", "Overview"
                ])

                analysis_section = extract_section(content_body, [
                    "日本の立ち位置", "立ち位置", "分析", "Analysis", "日本企業の先進事例", "Advanced Case", "Japan", "Domestic"
                ])

                if "Articles_2025" in str(base_dir):
                    category = md_file.parent.name
                    if category == "Articles_2025": category = "Articles_General"
                else:
                    category = base_dir.name

                vector_source_text = f"{md_file.stem}\n{summary_section}\n{analysis_section}\n{content_body}"
                embedding = model.encode(vector_source_text).tolist()

                doc_ref = db.collection('tech_docs').document(md_file.stem)
                doc_data = {
                    'title': md_file.stem,
                    'category': category,
                    'content': content_body,
                    'tags': metadata.get('tags', []),
                    'url': metadata.get('url', ''),
                    'rating': metadata.get('rating', None),
                    'date': date_val,
                    'summary_section': summary_section,
                    'analysis_section': analysis_section,
                    'embedding': embedding,
                    'updated_at': firestore.SERVER_TIMESTAMP
                }
                doc_ref.set(doc_data)

                extract_status = []
                extract_status.append("要約○" if summary_section else "要約×")
                extract_status.append("分析○" if analysis_section else "分析×")
                print(f"✅ [{category}] {md_file.name} -> {' '.join(extract_status)}")

            except Exception as e:
                print(f"❌ エラー: {md_file.name} - {e}")

if __name__ == "__main__":
    process_md_files()
    print("--- 構築完了 ---")
