import os
from pathlib import Path
from sentence_transformers import SentenceTransformer
import firebase_admin
from firebase_admin import credentials, firestore

# Firebase初期化
# serviceAccountKey.json をプロジェクトルートに配置してください
cred = credentials.Certificate("serviceAccountKey.json")
# Firebase Admin SDK の初期化
firebase_admin.initialize_app(cred) 
db = firestore.client()

# 埋め込みモデルの準備
# NOTE: RAGの検索精度は、このモデルに大きく依存します。
# 簡易構築のため MiniLM を使用していますが、Phase 2ではより高性能なモデルへの置き換えを推奨します。
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2') 

# scripts/build_vector_db.py の修正箇所

def process_md_files():
    """MDファイルを読み込み、ベクトル化してFirestoreに保存する"""
    
    # 1. 読み込み対象のルートディレクトリ
    md_dirs = [
        "./gartner_2025",
        "./nikkei_bp_2025_2035",
        "./次世代発電",
        "./自動車産業2045", # 👈 新規追加
        "./Articles_2025"   # サブフォルダを持つディレクトリ
    ]
    
    for md_dir_path in md_dirs:
        base_dir = Path(md_dir_path)
        
        if not base_dir.exists():
            print(f"⚠️ ディレクトリが見つかりません: {base_dir}")
            continue

        # 2. rglob("*.md") でサブディレクトリも含めて全検索
        for md_file in base_dir.rglob("*.md"):
            
            # 隠しファイル等はスキップ
            if ".git" in str(md_file) or ".firebase" in str(md_file):
                continue

            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 3. カテゴリ名の決定ロジック
                # Articles_2025 の場合は、直上のフォルダ名（AIinfoなど）をカテゴリにする
                if "Articles_2025" in str(base_dir):
                    category = md_file.parent.name
                    # 直下にファイルがあった場合の退避策
                    if category == "Articles_2025":
                         category = "Articles_General"
                else:
                    # その他のディレクトリは、指定したフォルダ名をそのままカテゴリにする
                    category = base_dir.name

                # ベクトル化
                embedding = model.encode(content).tolist()
                
                # Firestore保存
                doc_ref = db.collection('tech_docs').document(md_file.stem)
                doc_ref.set({
                    'title': md_file.stem,
                    'content': content,
                    'embedding': embedding,
                    'category': category, 
                    'updated_at': firestore.SERVER_TIMESTAMP
                })
                
                print(f"✅ [{category}] {md_file.name} をベクトル化")
            
            except Exception as e:
                print(f"❌ エラー: {md_file.name} - {e}")



if __name__ == "__main__":
    print("--- ベクトルデータベース構築を開始します ---")
    process_md_files()
    print("--- 構築完了 ---")
