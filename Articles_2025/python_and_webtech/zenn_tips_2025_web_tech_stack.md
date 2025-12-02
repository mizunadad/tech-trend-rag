---
title: "2025年版 スタートアップエンジニアが考えるWebアプリの技術選定"
url: https://zenn.dev/m_noto/articles/5e4c9f705f500b
date: 2025-10-15
tags:
  - Zenn
  - WebDevelopment
  - TechStack
  - TypeScript
  - NextJS
  - Frontend
---

# 2025年版 スタートアップエンジニアが考えるWebアプリの技術選定

URL: [https://zenn.dev/m_noto/articles/5e4c9f705f500b](https://zenn.dev/m_noto/articles/5e4c9f705f500b)
Published: 2025年10月15日頃
Author: _mino

---

## Original Content

この記事は、ムーザルちゃんねるさんの動画「2025年版『Webアプリ作るなら技術どれにする?』」を見て、筆者が今年を振り返り採用してよかった技術や、トレンドから見た来年以降流行りそうな技術についてまとめたもの。フロントエンド開発者の視点から、2025年の最新技術スタックを網羅的に紹介している。

### 主要な技術カテゴリー

#### 🧩 言語・フレームワーク
- **TypeScript**: Next.jsとの組み合わせが定番。初期の型定義整備が重要
- **Next.js**: v16ベータ版公開中。Turbopack安定版、React Compiler導入など大幅アップデート予定
- **Hono**: Web標準APIのみを使用した超高速・軽量フレームワーク。Cloudflare Workersとの相性抜群

#### 📚 スタイル・UIコンポーネント
- **TailwindCSS**: v4以降Lightning CSS統合によりパフォーマンス向上。AIとの相性が良い
- **ShadcnUI**: Radix UIベース。必要なコンポーネントのみインストール可能で軽量
- **HeroUI**: v3 Alpha版公開中。デフォルトデザインがリッチでそのまま使えるモダンなデザイン

#### 📌 バリデーション・状態管理
- **Valibot**: Zodより小さいバンドルサイズ、優れた型推論
- **Zustand**: シンプルな実装、学習コスト低。小〜中規模プロジェクトに最適

#### 🪪 認証
- **Clerk**: リッチなUIコンポーネント提供。無料枠充実
- **Supabase Auth**: RLS(行レベルセキュリティ)との組み合わせで強力なアクセス制御

#### 📊 データベース・ORM
- **Supabase Database**: PostgreSQLベース。RLSによるセキュリティ、コネクションプーリング最適化
- **PlanetScale**: 2025年9月PostgreSQL対応正式リリース。Git風ブランチング機能
- **Drizzle ORM**: TypeScript-first、SQLライクな構文。Studio、seed関数など便利機能が充実

#### ✉️ メール・通知
- **Resend**: React Emailとの相性良好。コンポーネントベースでリッチなテンプレート作成
- **Knock**: 複数チャネル通知を統合管理。ワークフローエンジンで複雑なロジック構築可能

#### 🪄 CMS
- **microCMS**: 日本製で直感的。日本語ドキュメント豊富
- **Payload**: TypeScript製オープンソース。Cloudflare Workersにワンクリックデプロイ対応

#### 🌅 画像管理
- **Cloud Storage**: Google Cloud内で完結。内部ネットワークでレイテンシ低
- **Cloudflare R2**: エグレス料金完全無料。データ配信量が多い場合に圧倒的コスト優位

#### ⏰ ホスティング
- **Vercel**: Next.js最適化。手軽だがコスト高め
- **Google Cloud Run**: Dockerコンテナベース。Vercelより安価、標準でログ収集

#### 🧱 バンドラー
- **Turbopack**: Next.js v16で安定版予定。Webpackより高速
- **Vite**: v7でRolldown(Rust製)実験導入。SPA開発に最適

#### 🚧 リンター・フォーマッター
- **Biome**: v2でさらに高速化。ESLint+Prettierを1ファイルで管理

#### 📝 テスト
- **Vitest**: Jest互換、Viteとの統合で設定ファイル共有
- **bun test**: v1.3リリース。最も高速なテストランナー

#### 🛎️ 監視・分析
- **Posthog**: オープンソース。セッションリプレイ、A/Bテスト、機能フラグを統合
- **Sentry**: 中・大規模向けエラートラッキング。信頼性高い

### 📗 番外編：注目技術
- **Rspack**: Webpack互換のRust製高速バンドラー
- **Oxlint**: Biomeより高速なRust製リンター
- **Vercel Fluid Compute**: 関数内同期処理実現、待機時間削減
- **ElectricSQL**: PostgreSQL同期エンジン。完全オフライン動作とゼロ遅延クエリ実現

---

## Summary

1. **TypeScript + Next.jsが2025年の主流スタック**: TypeScriptの型安全性とNext.js v16の大幅アップデート(Turbopack、React Compiler)により、開発体験が飛躍的に向上。フロントエンド開発の事実上の標準となっている

2. **軽量・高速化への強いトレンド**: Rust製ツール(Biome、Turbopack、Rspack、Oxlint)が台頭し、バンドルサイズ削減とビルド高速化が重視されている。Valibotのような軽量バリデーションライブラリも人気

3. **統合管理ツールの台頭**: Clerk(認証+組織管理)、Knock(複数チャネル通知統合)、Posthog(分析+A/Bテスト+機能フラグ)など、複数機能を統合したプラットフォームが開発効率向上に貢献

4. **コスト最適化への意識**: Cloudflare R2のエグレス料金無料、Google Cloud RunのVercelより安価な選択肢、Supabaseの低コストDB構築など、スタートアップにとってコスト効率が重要な選定基準となっている

5. **オープンソース&セルフホスティングの選択肢拡大**: Payload CMS、Posthog、Supabaseなど、オープンソースでセルフホスティング可能なツールが増加。拡張時のコスト増大を防ぎ、カスタマイズ性を高める戦略が可能に

---

## My Notes



---

## Rating

⭐⭐⭐⭐⭐ (5/5)

**評価理由**: 2025年の最新技術トレンドを網羅的かつ実践的に紹介。各技術の選定ポイントと補足情報が明確で、スタートアップのエンジニアにとって即座に活用できる内容。特にコスト面や開発体験の視点が実務的で価値が高い。
