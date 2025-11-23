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

def process_md_files():
    """MDファイルを読み込み、ベクトル化してFirestoreに保存する"""
    
    md_dirs = [
        "./gartner_2025",
        "./nikkei_bp_2025_2035"
    ]
    
    for md_dir in md_dirs:
        for md_file in Path(md_dir).glob("*.md"):
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # --- チャンキングはここではスキップし、ファイル全体をベクトル化 ---
            
            # ベクトル化（Embedding）
            embedding = model.encode(content).tolist()
            
            # Firestore保存
            # コレクション 'tech_docs' に保存
            doc_ref = db.collection('tech_docs').document(md_file.stem)
            doc_ref.set({
                'title': md_file.stem,
                'content': content,
                'embedding': embedding, # ベクトルデータ
                'category': md_dir.split('/')[-1],
                'updated_at': firestore.SERVER_TIMESTAMP
            })
            
            print(f"✅ {md_file.name} をベクトル化し、Firestoreに保存しました")

if __name__ == "__main__":
    print("--- ベクトルデータベース構築を開始します ---")
    process_md_files()
    print("--- 構築完了 ---")
