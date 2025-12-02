---
title: "ローカルRAGを手軽に構築できるMCPサーバを作りました"
url: "https://zenn.dev/mkj/articles/30eeb69bf84b3f"
date: 2025-11-06
tags: [readitlater, web-clip, MCP, RAG, PostgreSQL, pgvector, AI]
---

# ローカルRAGを手軽に構築できるMCPサーバを作りました

**🔗 URL**: [ローカルRAGを手軽に構築できるMCPサーバを作りました](https://zenn.dev/mkj/articles/30eeb69bf84b3f)  
**📅 Date**: 2025-11-06

## 📄 Original Content

松尾研究所のからあげ氏による、MCP（Model Context Protocol）とPostgreSQLのpgvectorを活用した完全ローカル動作可能なRAGシステム構築記事。CursorやWindsurfには標準搭載されているベクトル検索機能が、Cline（Roo Code）にはないことから、手軽にベクトル検索を実現するMCPサーバーを開発。OpenAI等の外部APIを一切使用せず、多言語対応のembeddingモデル（multilingual-e5-large）とpgvectorによる完全ローカル環境でのRAG構築を実現。PythonベースでLangChainなどの変化の激しいライブラリに依存せず、差分インデックス化により大量ドキュメントを効率管理。インデックス化はCLIツール、検索・クエリ操作はMCPインターフェースという明確な役割分担で構成されている。

## 🎯 Summary

- **完全ローカルRAGの実現**: OpenAI APIを使わず、multilingual-e5-largeとpgvectorで外部依存なしの完全ローカル環境での高精度ベクトル検索システムを構築
- **AIコーディングツール間のギャップ解消**: Cursor/Windsurfの標準機能とCline/Roo Codeの機能差を埋め、どのツールでも統一的なRAG検索体験を提供
- **差分インデックス化による効率性**: 新規・変更ファイルのみを処理する差分インデックス化機能で、大量ドキュメントの継続的な管理を低コストで実現
- **多様なドキュメント形式対応**: MarkItDownライブラリによりMarkdown、テキスト、PowerPoint、PDFなど多様な形式を統一的に処理可能
- **安定性重視の設計思想**: LangChainなど変化の激しいライブラリに依存せず、uvパッケージ管理とDockerベースの構成で長期的な保守性を確保

## 📊 主要機能一覧

| 機能カテゴリ | 機能詳細 | 実装技術 |
|---|---|---|
| **ベクトル検索** | 多言語対応のセマンティック検索 | PostgreSQL pgvector + multilingual-e5-large |
| **ドキュメント処理** | Markdown、テキスト、PPTX、PDF対応 | MarkItDown |
| **インデックス管理** | 全件・差分・特定ディレクトリ対応 | CLI（Python） |
| **検索インターフェース** | MCP経由での検索クエリ実行 | MCP Server |
| **多言語サポート** | 日本語を含む多言語ドキュメント対応 | multilingual-e5-large |

## 📊 システム構成と処理フロー

| フェーズ | 処理ステップ | 担当コンポーネント | 技術要素 |
|---|---|---|---|
| **インデックス化** | 1. ドキュメント取得 | CLI Tool | ファイルシステム |
| | 2. マークダウン変換 | Document Processor | MarkItDown |
| | 3. チャンク分割 | Document Processor | 可変チャンクサイズ |
| | 4. ベクトル生成 | Embedding Generator | multilingual-e5-large |
| | 5. DB保存 | RAG Service | PostgreSQL pgvector |
| **検索** | 1. クエリ受信 | MCP Interface | MCP Protocol |
| | 2. クエリベクトル化 | Embedding Generator | multilingual-e5-large |
| | 3. 類似度検索 | RAG Service | pgvector cosine similarity |
| | 4. 結果返却 | MCP Interface | JSON format |

## 📊 セットアップ手順

| ステップ | 作業内容 | コマンド | 備考 |
|---|---|---|---|
| 1. uvセットアップ | Pythonパッケージ管理 | `git clone && cd mcp-rag-server && uv sync` | 仮想環境自動構築 |
| 2. PostgreSQL起動 | Docker起動 | `docker run --name postgres-pgvector -e POSTGRES_PASSWORD=password -p 5432:5432 -d pgvector/pgvector:pg17` | pgvector拡張込み |
| 3. DB作成 | データベース初期化 | `docker exec -it postgres-pgvector psql -U postgres -c "CREATE DATABASE ragdb;"` | |
| 4. 環境変数設定 | .envファイル作成 | デフォルト設定で動作可能 | 必要に応じてカスタマイズ |
| 5. MCP設定 | MCPホスト設定 | mcp_settings.jsonに追加 | Cline/Cursor対応 |

## 📊 CLIコマンド一覧

| コマンド | 機能 | オプション例 |
|---|---|---|
| `python -m src.cli index` | 全件インデックス化 | - |
| `python -m src.cli index --directory ./path/to/documents` | 特定ディレクトリのインデックス化 | `--directory` |
| `python -m src.cli index --chunk-size 300 --chunk-overlap 50` | チャンクサイズ指定インデックス化 | `--chunk-size`, `--chunk-overlap` |
| `python -m src.cli index --incremental` | 差分インデックス化（新規・変更のみ） | `--incremental` |
| `python -m src.cli clear` | インデックスクリア | - |

## 📊 環境変数設定（.env）

| 変数名 | デフォルト値 | 説明 |
|---|---|---|
| POSTGRES_HOST | localhost | PostgreSQLホスト |
| POSTGRES_PORT | 5432 | PostgreSQLポート |
| POSTGRES_USER | postgres | データベースユーザー |
| POSTGRES_PASSWORD | password | データベースパスワード |
| POSTGRES_DB | ragdb | データベース名 |
| SOURCE_DIR | ./data/source | ソースドキュメントディレクトリ |
| PROCESSED_DIR | ./data/processed | 処理済みドキュメントディレクトリ |
| EMBEDDING_MODEL | intfloat/multilingual-e5-large | Embeddingモデル |

## 📊 トランスフォーマー関連知見（RAG検索実例）

記事内で松尾・岩澤研究室の勉強会スライド資料を使った検索例が示されており、以下の知見が抽出された：

| トピック | 主要知見 |
|---|---|
| **事前学習済みトランスフォーマーの汎用性** | 言語で訓練したトランスフォーマーは別のモダリティにも転移可能（FPT研究） |
| **性能特性** | モデルサイズが大きいほど性能向上、LSTMより大幅に優秀、言語事前学習が他モダリティより優位 |
| **Set Transformer** | SAB/ISAB/PMAで構成される集合データ処理用アーキテクチャ |
| **BigBird** | Random + Window + Global Attentionでスパース化、約8倍の長入力処理が可能 |

## 💭 My Notes

- 品質保証の観点から、完全ローカル環境でのRAG構築は機密性の高い技術文書管理に最適
- pgvectorの選択は、PostgreSQLの成熟したエコシステムを活用できる点で保守性・安定性が高い
- 差分インデックス化機能は、継続的に更新される設計文書やテスト結果の管理に有効
- LangChain非依存の設計思想は、長期運用を考慮した品質管理システムとして評価できる
- multilingual-e5-largeによる多言語対応は、日英混在の技術文書が多い半導体業界での実用性が高い
- MCPによるインターフェース標準化は、将来的なAIツールの切り替えコストを低減
- データ分析業務での過去分析結果やPythonコード資産との連携により、分析ナレッジの体系的蓄積が可能

## ⭐ Rating
Important: ⭐⭐⭐⭐⭐

---

**GitHubリポジトリ**: https://github.com/karaage0703/mcp-rag-server