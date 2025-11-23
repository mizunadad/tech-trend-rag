---
title: T6-06-04 OAuth/OpenID Connect・フェデレーション認証
url: https://openid.net/developers/how-connect-works/
date: 2025-11-02
tags:
  - デジタルID
  - OAuth
  - OpenID-Connect
  - SSO
  - シングルサインオン
  - フェデレーション認証
  - T6-06-04
rating: 5
---

# T6-06-04 OAuth/OpenID Connect・フェデレーション認証

## Summary(5つの要点)

1. **シングルサインオン(SSO)の実現**: 一度のログインで複数サービスを利用できる標準プロトコル。GoogleやAppleなどの認証基盤を活用し、ユーザーはサービスごとのID/パスワード管理から解放される
2. **OAuth 2.0による権限委譲**: アプリケーションがユーザーのパスワードを知ることなく、限定的なアクセス権限を取得できる仕組み。Googleドライブ連携、SNS投稿、決済連携などで広く活用
3. **OpenID Connectによる本人確認**: OAuth 2.0の拡張として、認証(Authentication)機能を追加。ID Token(JWT形式)によりユーザー属性情報(氏名、メールアドレス等)を安全に取得
4. **企業間ID連携の基盤**: SAML 2.0に代わる次世代プロトコルとして、企業間のフェデレーション認証に活用。Microsoft Entra ID(旧Azure AD)、Okta、Auth0などのIdP(Identity Provider)が標準サポート
5. **セキュリティと利便性の両立**: PKCE(Proof Key for Code Exchange)、State Parameter、Nonce等のセキュリティ機能により、中間者攻撃・CSRF攻撃を防止しつつ、ユーザー体験を損なわない設計

## 具体的プロダクト事例

### 日本企業の先進事例

1. **Yahoo! JAPAN ID連携 - 国内最大級のOpenID Connect基盤**
   - [月間アクティブユーザー8,400万人のID基盤](https://id.yahoo.co.jp/)
   - 概要: Yahoo! JAPAN IDを認証基盤として、PayPay、ZOZO、LINE等の外部サービスとID連携。OpenID Connect準拠のシングルサインオンを提供
   - 実績: 連携サービス1,000以上。Yahoo!ショッピング、ヤフオク!、PayPayモールなどでシームレスな買い物体験を実現

2. **LINE Login - ソーシャルログインの国内標準**
   - [月間アクティブユーザー9,600万人のID連携](https://developers.line.biz/ja/services/line-login/)
   - 概要: LINEアカウントを利用した簡単ログイン機能。OpenID Connect準拠で、氏名・メールアドレス・プロフィール画像を取得可能
   - 実績: ECサイト、ニュースメディア、自治体アプリなど、連携サービス数万件。ユーザーはLINEアカウントのみで多様なサービスを利用

3. **NTTドコモ dアカウント - 通信キャリアID基盤**
   - [契約者数8,000万人超のキャリアID](https://www.docomo.ne.jp/)
   - 概要: ドコモユーザー以外も利用可能な共通ID基盤。OpenID Connect対応で、d払い、dポイント、dマーケット等のサービスとシームレス連携
   - 実績: dアカウント会員数4,000万人以上。コンビニ決済、動画配信、音楽配信など幅広いサービスで採用

4. **サイボウズ - kintone OAuth連携エコシステム**
   - [業務アプリプラットフォームのAPI連携基盤](https://cybozu.co.jp/kintone/)
   - 概要: kintone(業務アプリ作成プラットフォーム)で、OAuth 2.0によるAPI連携を提供。Slack、Gmail、Salesforceなど100以上の外部サービスとデータ連携
   - 実績: 導入企業25,000社以上。ワークフロー自動化、データ同期、通知連携など多様なユースケース

5. **freee - 会計ソフトのAPI連携エコシステム**
   - [OAuth 2.0による銀行API・クレジットカードAPI連携](https://www.freee.co.jp/)
   - 概要: 銀行口座・クレジットカード明細を自動取得し、会計仕訳を自動化。OAuth 2.0により、ユーザーのパスワードを預からずに安全に連携
   - 実績: 連携金融機関3,600以上。中小企業・個人事業主100万以上が利用

### グローバルスタンダード

1. **Google Identity Platform - 世界最大級のOpenID Connect基盤**
   - [20億以上のGoogleアカウントによるSSO](https://developers.google.com/identity)
   - 概要: Googleアカウントを認証基盤として、YouTube、Gmail、Google Drive等のサービスとシームレス連携。OpenID Connect準拠で、第三者アプリにも認証基盤を提供
   - 実績: 「Sign in with Google」ボタンは世界中の数百万のWebサイト・アプリに実装。開発者向けにFirebase Authenticationも提供

2. **Apple Sign In - プライバシー重視のSSO**
   - [iOS 13以降で標準搭載、10億デバイスに展開](https://developer.apple.com/sign-in-with-apple/)
   - 概要: Apple IDによるワンタップログイン。ユーザーは実メールアドレスを隠し、Appleが生成した匿名メールアドレスを使用可能。OpenID Connect準拠
   - 実績: App Storeのアプリ審査で、第三者ログインを実装する場合は「Sign in with Apple」の実装が必須化(2020年~)

3. **Microsoft Entra ID(旧Azure AD) - エンタープライズSSO基盤**
   - [5億以上のアクティブユーザー、企業向けID管理の標準](https://www.microsoft.com/en-us/security/business/identity-access/microsoft-entra-id)
   - 概要: OpenID Connect、SAML 2.0をサポートし、Office 365、Teams、Dynamics 365などのMicrosoftサービスと、Salesforce、ServiceNow等の数千のSaaSアプリとSSO連携
   - 実績: Fortune 500企業の95%が採用。条件付きアクセス、多要素認証(MFA)、リスクベース認証を統合

4. **Okta - クラウドIDaaS(Identity as a Service)のリーダー**
   - [7,000以上のSaaSアプリとプリ統合済みSSO](https://www.okta.com/)
   - 概要: OpenID Connect、SAML 2.0、OAuth 2.0をサポートし、企業向けSSO基盤を提供。アダプティブ多要素認証、ゼロトラストアクセス制御を統合
   - 実績: 導入企業19,000社以上(T-Mobile、20th Century Fox、LinkedIn等)。APIアクセス管理、カスタマーID管理にも対応

5. **Auth0(Okta傘下) - 開発者向けID管理プラットフォーム**
   - [月間10億以上のログインを処理](https://auth0.com/)
   - 概要: OpenID Connect、OAuth 2.0の実装を簡素化するSDKとAPI群を提供。ソーシャルログイン(Google、Facebook、GitHub等)、エンタープライズログイン(SAML、AD)、パスワードレス認証を統合
   - 実績: 開発者500万人以上が利用。Mazda、Atlassian、Mozilla等が採用

## My Notes

## Rating: 5/5

**評価理由**:
- 技術標準が確立し、グローバルで広範に実装されている
- ユーザー体験とセキュリティのバランスが優れている
- 日本企業・グローバル企業ともに実用化が進展
- エンタープライズからコンシューマーまで幅広いユースケースに対応
- 唯一の懸念は、Google・Apple・Microsoftへの過度な依存によるプラットフォームリスク

## 全体要約の特徴(5つの要点)

1. **パスワード疲労からの解放**: 平均的なユーザーは100以上のオンラインアカウントを保有し、パスワード管理が破綻。OAuth/OpenID ConnectによるSSOにより、ユーザーは1つのID(Google、Apple、LINE等)で複数サービスを利用可能。パスワードリセット対応コストは1件あたり70ドルと試算され、企業側にもメリット大
2. **権限委譲の標準化(OAuth 2.0)**: アプリケーションがユーザーのパスワードを知ることなく、限定的なアクセス権限(スコープ)を取得できる仕組み。「Googleドライブの読み取り専用権限」「Twitter投稿権限」など、きめ細かな権限制御が可能。アクセストークンの有効期限を設定し、セキュリティリスクを軽減
3. **認証と認可の分離(OpenID Connect)**: OAuth 2.0は本来「認可(Authorization)」のプロトコルだが、OpenID Connectが「認証(Authentication)」機能を追加。ID Token(JWT形式)により、ユーザー属性情報(sub、name、email等)を暗号署名付きで取得。改ざん検知が可能
4. **エンタープライズID連携の標準**: SAML 2.0(2005年策定)に代わり、OpenID ConnectがエンタープライズID連携の主流に。Microsoft Entra ID、Okta、Auth0などのIdPが標準サポート。JSONベースで軽量、REST APIとの親和性が高く、モダンなWebアプリに最適
5. **セキュリティ機能の充実**: PKCE(ネイティブアプリの認可コード横取り攻撃を防止)、State Parameter(CSRF攻撃防止)、Nonce(リプレイ攻撃防止)、Token Binding(トークン盗聴防止)など、実用レベルのセキュリティ対策が標準化

## 日本の立ち位置・強み・弱み(4つの要点)

### 強み

1. **国内プラットフォームの確立**: Yahoo! JAPAN ID(8,400万MAU)、LINE(9,600万MAU)、dアカウント(4,000万会員)など、日本独自の大規模ID基盤が構築され、国内サービスとの連携エコシステムが成熟。Google・Appleに依存しない選択肢を提供
2. **金融API連携の進展**: 銀行法改正(2018年)によりオープンAPIが義務化され、freee、マネーフォワード、Zaim等のFinTechサービスが、OAuth 2.0により銀行口座・クレジットカード明細を安全に取得。欧州PSD2(決済サービス指令)と同様の制度整備

### 弱み

1. **グローバルプラットフォームへの依存**: 日本のWebサイト・アプリの多くが「Sign in with Google」「Sign in with Apple」を実装し、実質的に米国企業のID基盤に依存。Yahoo! JAPAN、LINEも国内市場に限定され、グローバル展開は不十分。海外サービスとのID連携で不利
2. **エンタープライズSSO市場の遅れ**: Microsoft Entra ID、Okta、Auth0などのグローバルIdP製品が日本企業にも浸透しているが、国産IdP(Cloudn、トラスト・ログイン)は機能・SaaSアプリ連携数で劣る。大企業の多くがMicrosoft依存となり、マルチベンダー戦略が困難

### グローバル比較と示唆

3. **EUのデジタル主権志向**: EUはeIDAS 2.0(2024年施行)により、Google・Appleに依存しない欧州独自のデジタルIDウォレットを構築。OpenID Connectを基盤としつつ、EU加盟国政府が発行するIDを優先。日本もデジタル主権の観点から、マイナンバーカードとOpenID Connectの統合を検討すべき
4. **中国のWeChat/Alipay一強**: 中国ではWeChat(12億MAU)、Alipay(10億MAU)が事実上のデジタルID基盤となり、決済・行政手続き・医療・交通など全てを統合。日本はYahoo!、LINE、dアカウントが分散し、統合的なエコシステム構築で後れ
