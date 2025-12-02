---
title: "Claude CodeのHooksは設定したほうがいい"
url: "https://syu-m-5151.hatenablog.com/entry/2025/07/14/105812"
date: 2025-07-14
tags: [readitlater, web-clip]
---

# Claude CodeのHooksは設定したほうがいい

**🔗 URL**: [Claude CodeのHooksは設定したほうがいい](https://syu-m-5151.hatenablog.com/entry/2025/07/14/105812)  
**📅 Date**: 2025-07-14

## 📄 Original Content
Claude Codeユーザーが実際にHooks機能を使い込んで得た知見をまとめた実体験ベースの記事。Claude Codeは優秀だが「記憶喪失する新人エンジニア」のような特性があり、CLAUDE.mdに重要事項を書いても忘れてしまう問題を、Hooks機能でシステムレベルで自動化・制御することで解決する方法を詳しく解説。4つのイベントタイプ（PreToolUse、PostToolUse、Notification、Stop）の使い分け、セキュリティ上の注意点、実用的な設定例（自動フォーマット、危険コマンド防止、テスト自動実行）、JSON制御による高度な制御方法まで、開発現場で即座に活用できる具体的なノウハウが満載。

## 🎯 Summary
- **自動フォーマット徹底**: 「フォーマッター忘れた」をゼロに。PostToolUseでJS/TS/Rustなど任意言語のファイル編集後に自動フォーマッター実行でコード品質を担保
- **危険操作の事前防止**: PreToolUseで`rm -rf`や本番環境ファイル編集をシステムレベルでブロック。CI到達前にローカルで問題を解決する「シフトレフト」の実現
- **フィードバックループ短縮**: 編集→CI失敗→修正（5-10分）から編集→即座に修正（数秒）へ。1日の積み重ねで50-100分の時間短縮を実現
- **JSON制御による高度な自動化**: exit code 2でClaude Codeに自動フィードバック、decision/reason/continueフィールドでAIの動作を細かく制御可能
- **開発ワークフロー統合**: Git Hooksより設定が簡単で、MCP連携、通知カスタマイズ、作業履歴記録など開発プロセス全体を自動化・最適化

## 📊 Hook Events一覧

| イベント | タイミング | 主な用途 | 制御可能性 |
|---|---|---|---|
| PreToolUse | ツール実行前 | 危険操作防止、権限チェック | 実行ブロック可能 |
| PostToolUse | ツール実行後 | 自動フォーマット、テスト実行 | フィードバック送信可能 |
| Notification | 通知送信時 | カスタム通知システム | 外部システム連携 |
| Stop | 応答完了前 | 作業サマリー、完了チェック | 処理継続指示可能 |

## 💻 実用的な設定例

### 1. 自動フォーマッター（JavaScript/TypeScript）
```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Write|Edit|MultiEdit",
      "hooks": [{
        "type": "command",
        "command": "jq -r '.tool_input.file_path | select(endswith(\".js\") or endswith(\".ts\"))' | xargs -r prettier --write"
      }]
    }]
  }
}
```

### 2. 危険コマンド防止
```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Bash",
      "hooks": [{
        "type": "command",
        "command": "jq -r 'if .tool_input.command | test(\"rm -rf|dd if=|:(){ :|:& };:\") then {\"decision\": \"block\", \"reason\": \"危険なコマンドは実行できません。\"} else empty end'"
      }]
    }]
  }
}
```

### 3. 本番環境ファイル保護
```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Write|Edit",
      "hooks": [{
        "type": "command",
        "command": "jq -r 'if .tool_input.file_path | test(\"production|.env|secrets\") then {\"decision\": \"block\", \"reason\": \"本番環境のファイルは触るな！\"} else empty end'"
      }]
    }]
  }
}
```

## 💭 My Notes
- 
- 

## ⭐ Rating
Important: ⭐⭐⭐⭐⭐

---