---
title: "GitHub Copilotの機能関連リリースまとめ"
url: "https://zenn.dev/dehio3/articles/33b545cb3ecfa9"
date: 2025-11-03
tags: [GitHub, Copilot, AI, MCP, 開発ツール, コード生成, 生成AI]
---

# GitHub Copilotの機能関連リリースまとめ

**URL**: [GitHub Copilotの機能関連リリースまとめ](https://zenn.dev/dehio3/articles/33b545cb3ecfa9)  
**取得日**: 2025-11-03

## Original Content

2025年6月から10月にかけてのGitHub Copilot機能アップデートを時系列でまとめた記事。GitHub Copilot Extensions（GitHub Apps形式）が2025年11月10日に廃止され、Model Context Protocol（MCP）サーバーへの移行が決定。GitHub MCP レジストリがローンチされ、AIツールの発見・統合が容易になった。

主要な機能強化として、Copilot Coding Agentが一般公開（2025年9月25日）され、issueの自動解決、プルリクエストの自動作成、Web検索機能、コンテキスト記憶機能などが追加された。また、GitHub Copilot CLIがパブリックプレビューとなり、コマンドライン上でのAI支援開発が強化された。

Visual Studio Code向けには、モデル自動選択機能が追加され、タスクに応じて最適なAIモデルが自動的に選択されるようになった。これにより、プレミアムリクエストの使用量が最適化される。

カスタマイズ機能も大幅に強化され、AGENTS.md、.instructions.md、copilot-instructions.mdなど複数の形式でリポジトリ固有の指示を記述可能に。プロジェクトの特定部分に異なる指示を適用できるようになった。

Copilot Code Reviewでは、自動コードレビュー機能が独立したリポジトリルールとして有効化可能になり、パスごとのカスタム指示、組織レベルの指示もサポートされた。

課金モデルも改善され、Copilot Coding Agentは1セッションにつき1プレミアムリクエストのみ使用するように変更。変更ファイル数や複雑さに関係なく、コスト予測が容易になった。

## Summary

1. **MCP移行の重要性**: GitHub Copilot Extensionsは2025年11月10日廃止。Model Context Protocol（MCP）サーバーへの移行が必須となり、GitHub MCPレジストリから各種AIツールを発見・統合可能

2. **Copilot Coding Agent一般公開**: issueから自動的にプルリクエストを生成、Web検索でコンテキスト補完、同一PR内のコンテキスト記憶など、エージェント機能が大幅強化され実用レベルに

3. **自動モデル選択機能**: VS Codeで「自動」オプションを選択すると、タスクに応じて最適なAIモデルを自動選択。プレミアムリクエストの使用量を最適化し、コスト効率向上

4. **カスタマイズの柔軟性**: AGENTS.md、.instructions.md、copilot-instructions.mdなど複数形式でリポジトリ固有の指示を記述可能。ディレクトリごとに異なる指示を適用でき、プロジェクト特性に最適化

5. **開発効率化の実践**: GitHub Copilot CLIによるコマンドライン統合、自動コミットメッセージ生成、独立した自動コードレビュールールなど、開発ワークフロー全体をAIが支援する環境が整備

## My Notes

（ここに自分の気づきやアイデアを記入）

バイブコーディングの実践環境として：
- AGENTS.mdでの品質基準定義（半導体テスト仕様、エラーハンドリング規約など）
- MCP統合で社内ツール（テスト装置API、品質データベース）との連携可能性
- 1セッション1リクエストの課金モデルで、複雑なテストスクリプト生成もコスト予測しやすい

## Rating

⭐⭐⭐⭐⭐ (5段階評価)
