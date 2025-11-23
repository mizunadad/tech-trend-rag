---
title: T6-06-02 分散型ID・SSI(Self-Sovereign Identity)
url: https://www.w3.org/TR/did-core/
date: 2025-11-02
tags:
  - デジタルID
  - DID
  - SSI
  - 分散型ID
  - 自己主権型アイデンティティ
  - ブロックチェーン
  - Web3
  - T6-06-02
rating: 3
---

# T6-06-02 分散型ID(DID)・SSI(Self-Sovereign Identity)

## Summary(5つの要点)

1. **中央集権からの脱却**: 中央の認証機関(IdP)に依存せず、個人が自分のIDを自律的に管理する次世代デジタルID。ブロックチェーン等の分散台帳技術を活用し、プライバシー保護と相互運用性を両立
2. **W3C標準化の進展**: 2022年7月、W3CがDecentralized Identifiers(DIDs) v1.0を正式勧告。Verifiable Credentials(VC) v2.0と組み合わせ、SSI(Self-Sovereign Identity)の実装基盤が確立
3. **爆発的な市場成長予測**: 世界のSSI市場規模は2024年13億ドルから2032年には449.8億ドルに達すると予測され、年平均成長率(CAGR)84.50%の急拡大が見込まれる
4. **トライアングルモデルの実装**: Issuer(発行者)・Holder(保有者)・Verifier(検証者)の3者モデルで、個人はデジタルウォレットに証明書(VC)を保管し、必要時に提示。発行者・検証者が個人の行動を追跡できないプライバシー設計
5. **150以上のDIDメソッド**: did:ion(Bitcoin)、did:ethr(Ethereum)、did:web(Web-based)など、用途に応じた多様なDIDメソッドが開発され、相互運用性を保ちつつ柔軟な実装が可能

## 具体的プロダクト事例

### 日本企業の先進事例

1. **NTTデジタル - ID & Trust Platform**
   - [分散型IDとゼロトラストを統合したエンタープライズ向けプラットフォーム](https://www.nttdata.com/jp/ja/)
   - 概要: DID/VC技術を活用し、企業間データ連携における本人確認・属性証明を提供。ゼロトラストアーキテクチャと統合したセキュリティソリューション
   - 実績: 金融機関のKYC(顧客確認)業務、サプライチェーン管理での実証実験を実施

2. **DataSign - トラストサービス基盤**
   - [日本初の包括的SSI/DIDプラットフォーム](https://datasign.jp/)
   - 概要: W3C標準に準拠したDID/VCプラットフォームを提供。教育機関の卒業証明書、企業の在籍証明書などのデジタル化を支援
   - 実績: 大学・専門学校での学位証明書デジタル化、人材業界での職歴証明に活用

3. **富士通 - ConnectionChain**
   - [ブロックチェーンベースの資格証明プラットフォーム](https://www.fujitsu.com/jp/)
   - 概要: Hyperledger Indy/Ariesを活用したDID/VC基盤。資格証明書、会員証、学習履歴などをデジタル証明書として発行・検証
   - 実績: 製造業のサプライチェーン認証、医療従事者の資格確認での実証

4. **三菱UFJ信託銀行 - デジタル証券とDID連携**
   - [Progmat(プログマ)でのDID活用検討](https://www.tr.mufg.jp/)
   - 概要: デジタル証券発行基盤Progmatにおいて、投資家のKYC情報をDID/VCで管理する構想を研究
   - 実績: ブロックチェーン証券の実証実験でDIDによる本人確認を試験導入

5. **JPYC - ステーブルコインとSSI連携**
   - [日本円ステーブルコインでのDID活用](https://jpyc.jp/)
   - 概要: 日本円連動ステーブルコインJPYCの取引において、DID/VCを活用したAML/CFT(マネーロンダリング対策)を検討
   - 実績: Web3ウォレットとの統合、分散型取引所(DEX)での本人確認に向けた研究開発

### グローバルスタンダード

1. **EU Digital Identity Wallet - eIDAS 2.0**
   - [EU全域での統一デジタルIDウォレット](https://digital-strategy.ec.europa.eu/en/policies/eidas-regulation)
   - 概要: 2024年施行のeIDAS 2.0規則により、EU加盟国27カ国でDID/VCベースのデジタルIDウォレットを導入。運転免許証、学位証明書、医療記録などを統合管理
   - 実績: 2026年までに全EU市民4.5億人への提供を目指す。国境を越えた行政・民間サービス利用が可能

2. **Microsoft Entra Verified ID(旧Azure AD Verifiable Credentials)**
   - [エンタープライズ向けDID/VCプラットフォーム](https://www.microsoft.com/en-us/security/business/identity-access/microsoft-entra-verified-id)
   - 概要: W3C標準準拠のDID/VCを企業認証に統合。従業員証明書、資格証明、パートナー企業認証などに活用。did:ionメソッド(Bitcoin)を採用
   - 実績: NHS(英国国民保健サービス)がCOVID-19ワクチン証明書に採用。グローバル企業数百社が導入

3. **Hyperledger Indy/Aries - オープンソースSSI基盤**
   - [Linux Foundationによる分散型ID基盤](https://www.hyperledger.org/use/hyperledger-indy)
   - 概要: 許可型ブロックチェーンをベースとしたDID/VCフレームワーク。ZKP(ゼロ知識証明)により最小限の情報開示で属性証明が可能
   - 実績: カナダBC州政府のOrgBook(企業登記証明)、英国NHS(医療従事者資格証明)、ドイツ連邦政府ID Unionなどで採用

4. **Sovrin Network - 公共DIDネットワーク**
   - [非営利団体運営のパブリックDID基盤](https://sovrin.org/)
   - 概要: Hyperledger Indyをベースとした公共DIDネットワーク。Sovrin Foundationがガバナンスを管理し、グローバルなSSI相互運用性を実現
   - 実績: 70カ国以上で利用。金融機関のKYC、政府機関の市民ID、教育機関の学位証明などに活用

5. **uPort/Veramo(ConsenSys) - EthereumベースDIDプラットフォーム**
   - [did:ethrメソッドの先駆者](https://veramo.io/)
   - 概要: Ethereumブロックチェーンを活用したDID/VCプラットフォーム。スマートコントラクトと連携し、DeFi、DAO、NFTマーケットプレイスでの本人確認に対応
   - 実績: Zug市(スイス)のデジタル市民ID、南アフリカの学位証明書デジタル化に採用

## My Notes

## Rating: 3/5

**評価理由**:
- W3C標準化により技術基盤は確立し、EU、北米で実証実験・本格導入が進展
- プライバシー保護と相互運用性を両立した革新的アーキテクチャ
- 日本では研究開発・実証段階にとどまり、社会実装は限定的
- 技術的複雑性、ユーザー教育、規制整備の課題が残存

## 全体要約の特徴(5つの要点)

1. **中央集権型IDの限界を克服**: GoogleやFacebookなどのIdP(Identity Provider)がユーザー行動を把握できる従来のID連携モデル(OpenID Connect)から脱却。SSIでは個人がデジタルウォレット内に証明書を保管し、必要時にのみ提示することで、プライバシーを最大限保護
2. **W3C標準化による相互運用性**: DIDs v1.0(2022年7月勧告)とVerifiable Credentials v2.0により、異なるDIDメソッド・VCフォーマット間での相互運用が可能。150以上のDIDメソッドが開発され、用途に応じた選択が可能
3. **トライアングルモデルの実装**: Issuer(証明書発行者:大学、政府、企業)、Holder(証明書保有者:個人)、Verifier(検証者:サービス提供者)の3者モデル。中央管理者を介さず、Holder主導で証明書を管理・提示
4. **ZKP(ゼロ知識証明)による最小開示**: 必要最小限の属性のみを開示する選択的開示(Selective Disclosure)とZKPにより、「20歳以上であること」を生年月日を開示せずに証明可能。GDPRのデータ最小化原則に合致
5. **ブロックチェーンの選択的活用**: DIDはブロックチェーンに限定されず、did:web(Web-based)、did:key(Key-based)など多様な実装が可能。一方、改ざん耐性が求められる用途ではBitcoin(did:ion)、Ethereum(did:ethr)、Hyperledger Indy等の分散台帳を活用

## 日本の立ち位置・強み・弱み(4つの要点)

### 強み

1. **先端技術研究の蓄積**: NTTデータ、富士通、日立などの大手IT企業が早期からDID/VC技術の研究開発に着手。2020年頃から実証実験を開始し、技術的知見を蓄積。特にエンタープライズ向けDIDプラットフォームで一定の成果
2. **マイナンバーカード基盤との連携可能性**: 公的個人認証(JPKI)とDID/VCを組み合わせることで、公的証明書と民間証明書を統合管理できるハイブリッドモデルの構築が可能。政府主導の信頼基盤を活用できる点は強み

### 弱み

1. **社会実装の遅れ**: EU eIDAS 2.0(2024年施行)、カナダOrgBook、英国NHS等が既に本格運用を開始している一方、日本ではDataSign、NTTデータ等の実証実験にとどまる。法制度整備(電子署名法、個人情報保護法との整合性)が不十分で、企業の導入判断が困難
2. **Web3エコシステムの脆弱性**: DID/VCはWeb3(分散型Web)の基盤技術だが、日本ではDeFi、DAO、NFTマーケットプレイスなどのWeb3サービスが規制により発展が阻害されている。暗号資産規制の厳格さがDID普及の足かせに

### グローバル比較と示唆

3. **EUの先行優位**: eIDAS 2.0により、EU全域でDID/VCベースのデジタルIDウォレットが2026年までに4.5億人に提供予定。国境を越えた相互運用性を法制度で担保し、民間企業も参画しやすい環境を整備。日本は法制度整備で5年以上の遅れ
4. **北米のエンタープライズ導入加速**: Microsoft Entra Verified ID、IBM Digital Health Pass、Workday Credentialsなど、グローバル企業がDID/VCを従業員認証・パートナー企業認証に採用。日本企業は実証実験段階にとどまり、グローバル標準から取り残されるリスク
