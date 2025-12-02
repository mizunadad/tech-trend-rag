---
title: "Codex CLIにClaude Codeから手軽に設定を移行する方法"
url: "https://zenn.dev/karaage0703/articles/aabaa01cb71647"
date: 2025-09-16
tags: [readitlater, web-clip, AI-tools, CLI, MCP]
---

# Codex CLIにClaude Codeから手軽に設定を移行する方法

**🔗 URL**: [Codex CLIにClaude Codeから手軽に設定を移行する方法](https://zenn.dev/karaage0703/articles/aabaa01cb71647)  
**📅 Date**: 2025-09-16

## 📄 Original Content

Claude CodeからCodex CLIへの設定移行手順を解説した技術記事。GPT5の登場とClaude Codeの性能低下を背景に、Codex CLIが注目される中での実践的な移行方法を提供。MCPサーバーの設定移行、スラッシュコマンドの移行、通知設定など、手動作業を最小限に抑えた効率的な移行プロセスを詳細に説明。特にmmcpとccmcpという自作ツールを活用してTOML形式への変換作業を自動化し、多くのAIエージェント間でのポータビリティを確保する方法論を提示している。

## 🎯 Summary

- **MCPサーバー移行の自動化**: ccmcpとmmcpツールを組み合わせることで、Claude CodeのJSON形式設定をCodex CLIのTOML形式に自動変換し、手動での設定書き直し作業を回避
- **2ステップ移行プロセス**: ①Claude CodeにuserスコープでMCPサーバー設定→②ccmcp export-to-mmcp、mmcp agents add codex-cli、mmcp applyコマンドで一括移行を実現
- **スラッシュコマンド簡単移行**: `cp -r ~/.claude/commands/* ~/.codex/prompts`でマークダウンファイルを直接コピーするだけで、Claude CodeのスラッシュコマンドをCodex CLIに移植可能
- **ベンダーロックイン回避戦略**: 各AIエージェントの独自機能を避け、MCPのようなオープン規格・デファクトスタンダードを優先することで将来の移行コストを最小化
- **実用的な設定例**: markitdown、arxiv-mcp-server、context7、gemini-google-searchなど必須MCPサーバーの具体的なセットアップコマンドと通知音設定を提供

## 📊 移行手順一覧表

| ステップ | 作業内容 | 使用ツール | 所要時間 |
|---|---|---|---|
| 1. Codex CLIセットアップ | `npm install -g @openai/codex` | npm | 2-3分 |
| 2. MCPサーバー移行 | ccmcp export-to-mmcp → mmcp apply | ccmcp, mmcp | 5分 |
| 3. スラッシュコマンド移行 | `cp -r ~/.claude/commands/* ~/.codex/prompts` | bash | 1分 |
| 4. 通知設定 | config.tomlに音声設定追加 | 手動編集 | 2分 |

## 📊 推奨MCPサーバー設定

| MCPサーバー | 機能 | セットアップコマンド |
|---|---|---|
| markitdown | ドキュメント変換 | `claude mcp add markitdown -s user -- uvx markitdown-mcp` |
| arxiv-mcp-server | 論文検索 | `claude mcp add arxiv-mcp-server -s user -- uvx arxiv-mcp-server` |
| context7 | コンテキスト管理 | `claude mcp add context7 -s user -- npx -y @upstash/context7-mcp` |
| gemini-google-search | Web検索 | `claude mcp add gemini-google-search -s user -e GEMINI_API_KEY=<key> GEMINI_MODEL=gemini-2.5-flash -- npx mcp-gemini-google-search` |

## 💭 My Notes

- ツール間の移行コストを考慮した設計思想は品質保証の観点でも重要
- MCPサーバーのuserスコープ設定が移行の前提条件となる点は設計制約として認識
- TOMLとJSON間の設定形式差異は自動化ツールで解決できる好例
- ベンダーロックイン回避のためのオープン規格採用は長期的な保守性向上に寄与

## ⭐ Rating
Important: ⭐⭐⭐⭐⭐

---