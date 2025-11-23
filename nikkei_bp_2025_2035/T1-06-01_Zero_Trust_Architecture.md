---
title: "T1-06-01 ゼロトラストアーキテクチャ"
url: "https://www.nist.gov/publications/zero-trust-architecture"
date: 2025-11-01
tags:
  - サイバーセキュリティ
  - ゼロトラスト
  - ネットワークセキュリティ
  - クラウドセキュリティ
  - T1-06-01
---

# T1-06-01 ゼロトラストアーキテクチャ

## ハイプ・サイクル位置づけ

**現在のフェーズ**: 実用期初期（2024-2027年）
**技術成熟度**: TRL 7-8（実証から初期展開段階）

## Summary（5つの要点）

1. **「何も信頼せず常に検証する」原則**: 従来の境界型防御（社内ネットワークは安全、外部は危険）から脱却し、すべてのアクセスを常に検証する新セキュリティモデル。内部からの脅威、ラテラルムーブメント（侵入後の横展開）を防止。

2. **アイデンティティベースの認証・認可**: ユーザー、デバイス、アプリケーション、データの4要素をアイデンティティとして管理。すべてのアクセスリクエストに対し、コンテキスト情報（場所、デバイス状態、リスクスコア）を評価して動的にアクセス制御。

3. **マイクロセグメンテーション**: ネットワークを細かく分割し、リソースごとに独立したアクセス制御を実施。侵入された場合でも被害範囲を最小化し、ラテラルムーブメントを阻止。

4. **継続的な監視とリスク評価**: ユーザーやデバイスの振る舞いを継続的に監視し、異常があれば即座にアクセスを遮断または追加認証を要求。SIEM（Security Information and Event Management）やUEBA（User and Entity Behavior Analytics）と連携。

5. **クラウド・リモートワーク時代の必須基盤**: テレワーク、クラウドSaaS利用の拡大により、従来の境界型防御が機能しない環境で有効。SASE（Secure Access Service Edge）、VPNレス接続、コンテナセキュリティと統合。

## 具体的プロダクト事例

### 日本企業の先進事例

#### 1. **NTTコミュニケーションズ「ゼロトラストセキュリティ on Flexible InterConnect」**
- **URL**: https://www.ntt.com/business/services/network/internet-connect/sd-wan/zero-trust.html
- **概要**: SD-WAN基盤上にゼロトラストセキュリティを実装したソリューション。
- **技術特徴**: 
  - CASB（Cloud Access Security Broker）、SWG（Secure Web Gateway）、ZTNA統合
  - 多要素認証、デバイス認証、証明書ベース認証
  - 日本国内データセンターでのセキュリティ処理（データ主権対応）
- **適用分野**: 大企業のグローバルネットワーク、金融機関、官公庁

#### 2. **富士通「FUJITSU Security Solution ゼロトラストセキュリティ」**
- **URL**: https://www.fujitsu.com/jp/solutions/business-technology/security/solutions/zero-trust/
- **概要**: エンドポイント、ネットワーク、データを統合管理するゼロトラストソリューション。
- **技術特徴**: 
  - EDR（Endpoint Detection and Response）、MDM（Mobile Device Management）統合
  - AI脅威検知エンジン
  - 富士通グループ13万人への適用実績
- **成果**: リモートワーク環境でのセキュリティインシデント50%削減

#### 3. **日立製作所「Lumada セキュリティソリューション」**
- **URL**: https://www.hitachi.co.jp/products/it/lumada/solution/security/index.html
- **概要**: OT（Operational Technology）環境を含むゼロトラスト実装。
- **技術特徴**: 
  - 制御システム、IoTデバイスへのゼロトラスト適用
  - 工場、インフラのサイバー・フィジカル統合セキュリティ
  - NIST SP 800-207準拠
- **適用分野**: 製造業、エネルギー、社会インフラ

#### 4. **ソフトバンク「ZTNA（Zero Trust Network Access）サービス」**
- **URL**: https://www.softbank.jp/biz/services/cloud/ztna/
- **概要**: VPNを置き換えるZTNAサービス。Netskope、Zscaler等のグローバルベンダー製品を提供。
- **技術特徴**: 
  - VPNレス接続（IPアドレス非公開）
  - SaaS、オンプレミス、クラウドへの統合アクセス制御
  - 最小権限の原則（Least Privilege Access）

### グローバルスタンダード

#### 1. **Palo Alto Networks「Prisma Access（SASE）」**
- **URL**: https://www.paloaltonetworks.com/sase
- **概要**: 世界シェアNo.1のSASEプラットフォーム。ゼロトラストとSD-WANを統合。
- **技術特徴**: 
  - 世界100以上のPoP（Point of Presence）からクラウドベースセキュリティ提供
  - AI脅威分析、機械学習型マルウェア検知
  - Zscaler、Netskope、Cloudflareと競合
- **導入実績**: フォーチュン100企業の70%以上、全世界8万5000社以上

#### 2. **Microsoft「Azure Active Directory + Conditional Access」**
- **URL**: https://learn.microsoft.com/en-us/azure/active-directory/conditional-access/
- **概要**: Microsoft 365、Azure環境のゼロトラスト実装基盤。
- **技術特徴**: 
  - アイデンティティベースのアクセス制御
  - リスクベース条件付きアクセス（デバイス、場所、サインインリスクスコア）
  - Intune（MDM/MAM）、Defender for Endpointと統合
- **普及**: Microsoft 365ユーザー3億4,500万人（2023年）

#### 3. **Google「BeyondCorp Enterprise」**
- **URL**: https://cloud.google.com/beyondcorp-enterprise
- **概要**: Googleが自社で10年以上運用したゼロトラストモデルを製品化。
- **技術特徴**: 
  - コンテキストアウェアアクセス制御
  - デバイス証明書ベース認証
  - Google Workspace、GCP環境への統合
- **特徴**: VPNを完全廃止したGoogle社内実績（全世界10万従業員）

#### 4. **Okta「Identity Cloud」**
- **URL**: https://www.okta.com/
- **概要**: クラウドベースのアイデンティティ・アクセス管理（IAM）プラットフォーム。
- **技術特徴**: 
  - SSO（シングルサインオン）、MFA（多要素認証）、ライフサイクル管理
  - 7,000以上のSaaS/アプリケーションと事前統合
  - Adaptive MFA（リスクベース認証）
- **導入実績**: フォーチュン100企業の85%、全世界18,000社以上

## My Notes

（ここに個人的な気づき、追加調査事項、関連技術リンク等を記入）

---

## Rating（5段階評価）

| 評価項目 | スコア | 備考 |
|---------|-------|------|
| **技術成熟度** | ★★★★☆ (4/5) | 大企業で実用化進展。中小企業への展開はこれから |
| **市場性・需要** | ★★★★★ (5/5) | テレワーク、クラウド移行で急拡大。2030年市場規模600億ドル予測 |
| **日本の競争力** | ★★★☆☆ (3/5) | ソリューション提供は進展。コア技術は米国ベンダー依存 |
| **社会実装の障壁** | ★★★☆☆ (3/5) | 既存システム刷新コスト、運用人材育成が課題 |
| **イノベーション性** | ★★★★★ (5/5) | セキュリティパラダイムシフト。今後10年の標準モデル |

**総合評価**: ★★★★☆ (4.0/5)

---

## 全体要約（5つの要点）

### 1. 技術の本質
ゼロトラストは「境界防御の終焉」を意味する。従来の「城と堀」モデル（社内ネットワークは安全、外部は危険）から、「すべてを疑い、すべてを検証する」モデルへの転換。クラウド、モバイル、IoT時代に適応したセキュリティ思想。

### 2. コア技術要素
- **IAM（Identity and Access Management）**: Okta、Azure AD、Ping Identity
- **ZTNA（Zero Trust Network Access）**: Zscaler Private Access、Cloudflare Access、Palo Alto GlobalProtect
- **CASB（Cloud Access Security Broker）**: McAfee MVISION Cloud、Netskope
- **SWG（Secure Web Gateway）**: Cisco Umbrella、Symantec WSS
- **EDR（Endpoint Detection and Response）**: CrowdStrike Falcon、Microsoft Defender

### 3. 応用分野
- **企業ネットワーク**: VPN置き換え、リモートアクセス
- **クラウド移行**: AWS、Azure、GCPへの安全なアクセス
- **M&A統合**: 異なる企業ネットワークの迅速な統合
- **OT/ICSセキュリティ**: 工場、インフラの制御システム保護
- **サプライチェーン**: パートナー企業、外部委託先とのセキュアな連携

### 4. 主要プレイヤー
- **米国**: Palo Alto Networks、Zscaler、Okta、Microsoft、Google、Cisco
- **日本**: NTTコミュニケーションズ、富士通、日立、ソフトバンク
- **欧州**: Fortinet、Check Point（イスラエル）
- **新興**: Cloudflare、Netskope、CrowdStrike

### 5. 将来展望
2026-2028年にかけて、ゼロトラストが企業セキュリティの標準モデルになる。SASE（Secure Access Service Edge）の普及により、ネットワークとセキュリティの融合が進展。量子暗号通信、耐量子暗号との統合により、ポスト量子時代のゼロトラストへ進化。2030年以降、IoT、OT環境へのゼロトラスト適用が本格化。

---

## 日本の立ち位置（4つの要点）

### 1. 強み：通信インフラとの統合

NTTグループは国内最大の通信キャリアとして、ネットワークとセキュリティを統合したゼロトラストソリューションを提供できる。NTT Comのゼロトラスト on Flexible InterConnectは、SD-WAN基盤上にSASE機能を実装しており、通信品質とセキュリティを同時保証。日立、富士通は製造業、社会インフラ向けにOT/ICSセキュリティを含むゼロトラスト実装で強み。ソニー、トヨタ等の大企業での導入実績が蓄積中。

### 2. 弱み：コア技術の海外依存

日本企業のゼロトラストソリューションは、Palo Alto、Zscaler、Okta、Microsoft等の米国ベンダー製品を統合・再販するSI（システムインテグレーション）型が多い。IAM、ZTNA、CASB等のコア技術を自社開発している日本ベンダーは少なく、技術の根幹を米国に依存。デバイス認証、リスクスコアリング、行動分析等のAIエンジンも海外製が主流。データ主権、安全保障の観点から、国産技術育成が急務。

### 3. 機会：デジタル庁・政府調達での展開

デジタル庁は「政府情報システムにおけるゼロトラストアーキテクチャ適用方針」（2022年）を公表し、中央省庁のゼロトラスト移行を推進。自治体、教育機関、医療機関へも波及する見込み。金融庁はFISC安全対策基準にゼロトラストを追記し、金融機関での導入が加速。製造業、インフラ事業者も経済安全保障の観点からゼロトラスト導入を検討中。国内市場の拡大がベンダー育成の好機。

### 4. 脅威：グローバルベンダーの市場支配

Palo Alto、Zscaler、Microsoft、Googleの4社で世界市場の70%以上を占有。これらのベンダーは巨額のR&D投資とM&Aにより技術優位を拡大中。日本企業が独自開発で対抗するのは困難。国産技術育成と並行して、グローバルベンダーとの戦略的提携、日本市場特有のニーズ（データローカライゼーション、法規制対応、日本語サポート）への対応で差別化が必要。

---

**作成日**: 2025-11-01  
**出典**: テクノロジーロードマップ2026-2035 第1章 T1-06-01  
**関連技術**: T1-06-02 AI脅威検知、T1-06-03 多要素認証、T1-06-04 量子暗号通信
