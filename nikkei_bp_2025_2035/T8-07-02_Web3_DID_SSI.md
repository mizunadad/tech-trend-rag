---
title: "T8-07-02 Web3・分散型ID（DID）・自己主権型アイデンティティ"
date: 2025-11-13
tags:
  - Web3
  - 分散型ID
  - DID
  - SSI
  - ブロックチェーン
  - プライバシー
  - データ主権
  - 暗号化
  - 品質保証
url: https://www.w3.org/TR/did-core/
---

# T8-07-02 Web3・分散型ID（DID）・自己主権型アイデンティティ

## ハイプ・サイクル位置づけ
**黎明期～期待のピーク期（2024-2025年)**
W3C標準化完了（2022年）により技術仕様は確立したが、実用化は初期段階。金融・医療・教育分野で実証実験が進行中。本格的な社会実装には5-10年を要すると予測される。

## 5つの要点Summary

1. **自己主権型アイデンティティ（SSI）の実現手段**: 中央管理者不要で個人がアイデンティティを管理する次世代インターネット基盤。ブロックチェーン上にID・証明書を記録し、プラットフォーム間で移動可能。GAFAM等の巨大IT企業によるデータ独占から脱却し、個人データの主権を取り戻す

2. **W3C標準化とVC（検証可能なクレデンシャル）**: 2022年にW3CがDID仕様を標準化。DIDとVC（Verifiable Credentials：検証可能なデジタル証明書）を組み合わせることで、学歴・資格・医療記録等の信頼性の高い情報共有が可能に。改ざん耐性と透明性を確保

3. **日本ではTrusted Web構想が政府主導**: 内閣官房デジタル市場競争本部が2020年から推進。個人・法人によるデータコントロール強化と、データ・相手方の検証可能性を実現。医療・サプライチェーン・人材分野で実証実験が進行

4. **グローバル事例**: Worldcoin（OpenAI CEO主導、2024年10月時点で690万人登録）、秋田犬デジタル血統書、金融KYC/AML対応、医療情報共有等で実用化開始。EU・米国・アジアで規制対応とプライバシー保護の両立が焦点

5. **品質保証の視点**: 秘密鍵管理のセキュリティ、ID紛失時の復旧手段、相互運用性（異なるDIDシステム間の互換性）、プライバシー保護（ゼロ知識証明等）が重要課題。Pythonによる暗号化実装・ブロックチェーン連携テストが実践スキル

## 具体的プロダクト事例

### 日本企業の先進事例

#### 内閣官房 Trusted Web推進協議会
- **URL**: https://trustedweb.go.jp/
- **概要**: 2020年10月から内閣官房デジタル市場競争本部が推進する、自己主権的なアイデンティティ管理を軸とした信頼性のあるデジタル空間構築プロジェクト
- **技術特徴**: 個人・法人によるデータのコントロール強化、やり取りするデータ・相手方を検証できる仕組みを構築。ブロックチェーンに依存しない柔軟なアーキテクチャ
- **実績**: 医療（患者同意管理）、サプライチェーン（トレーサビリティ）、人材（職歴証明）分野で実証実験を実施
- **適用分野**: 医療情報共有、金融KYC、教育証明、公的証明書発行

#### NEC 自己主権型アイデンティティソリューション
- **URL**: https://jpn.nec.com/fintech/contents/202304/Web3.0_wallet.pdf
- **概要**: NECが開発するSSI/DID技術を活用した個人情報管理プラットフォーム
- **技術特徴**: 分散型ID、VC（検証可能なクレデンシャル）、デジタルウォレットを統合。金融機関のKYC（本人確認）業務を効率化
- **実績**: 金融機関における本人確認プロセスの簡素化、マネーロンダリング対策（AML）への適用を検証
- **適用分野**: 金融KYC/AML、保険契約管理、医療情報共有

#### Meta Akita × Heirloom デジタル血統書
- **URL**: https://metameta.world/
- **概要**: DID/VC技術を用いた秋田犬のデジタル血統書。2024年3月から公益社団法人秋田犬保存会が正式導入
- **技術特徴**: ブロックチェーン上にDIDを記録し、血統書の偽造防止を実現。スマートフォンアプリで血統書を管理
- **実績**: 紙ベースの血統書管理からデジタル化。情報改ざん防止と国際的な信頼性向上を達成
- **適用分野**: ペット血統書管理、畜産トレーサビリティ、希少動物保護

#### デジタルガレージ × Blockchain Identity Lab
- **URL**: https://www.garage.co.jp/ja/pr/2021/01/20210128.html
- **概要**: デジタルガレージが参画するブロックチェーン・アイデンティティ研究所。DID技術の社会実装を推進
- **技術特徴**: Ethereum、Hyperledger IndyベースのDIDプロトコル開発。分散型アイデンティティの相互運用性を研究
- **実績**: 金融機関とのKYC実証実験、教育機関でのデジタル卒業証明書発行
- **適用分野**: 金融KYC、教育証明、電子契約、IoTデバイス認証

#### 富士通 Fujitsu Track and Trust
- **URL**: https://www.fujitsu.com/jp/solutions/industry/retail/retail-solutions/tracktrust/
- **概要**: サプライチェーン全体の透明性を確保するブロックチェーン基盤。DID技術でサプライヤー認証を実現
- **技術特徴**: 製品・原材料のトレーサビリティをブロックチェーンで管理。各サプライヤーにDIDを発行し、品質証明を検証可能に
- **実績**: 食品・医薬品のサプライチェーン管理、ESG情報開示支援
- **適用分野**: サプライチェーン管理、品質保証、ESG/SDGs情報開示

### グローバルスタンダード

#### W3C DID（Decentralized Identifiers）規格
- **URL**: https://www.w3.org/TR/did-core/
- **概要**: 2022年にW3C（World Wide Web Consortium）が標準化した分散型識別子の国際規格
- **技術特徴**: 中央管理者不要で、個人・法人・IoTデバイスが固有のIDを持ち、検証可能なクレデンシャル（VC）と組み合わせて信頼性を担保
- **実績**: HTTP、HTML、CSSを標準化したW3Cによる公式規格。グローバルで採用が進む
- **適用分野**: あらゆる分野のデジタルアイデンティティ基盤

#### Worldcoin（World ID）
- **URL**: https://worldcoin.org/
- **概要**: OpenAI CEO サム・アルトマン氏が設立した生体認証ベースのグローバルDIDプロジェクト
- **技術特徴**: 虹彩スキャン（Orb）で生体認証を行い、World IDを発行。AI時代の「人間証明」を実現し、ボットとの区別を可能に
- **実績**: 2023年7月開始以来、2024年10月時点で690万人以上が登録。暗号資産WLD配布でインセンティブ設計
- **適用分野**: AI時代の本人確認、UBI（ユニバーサルベーシックインカム）配布、デジタル投票

#### Microsoft Entra Verified ID（旧Azure Active Directory Verifiable Credentials）
- **URL**: https://www.microsoft.com/en-us/security/business/identity-access/microsoft-entra-verified-id
- **概要**: Microsoft提供の企業向けDID/VCソリューション。Azure Active Directoryと統合
- **技術特徴**: W3C DID標準準拠。企業の従業員・パートナーにVCを発行し、ゼロトラストセキュリティを実現
- **実績**: 多国籍企業での従業員ID管理、教育機関でのデジタル卒業証明書発行
- **適用分野**: 企業ID管理、教育証明、サプライチェーン認証

#### Sovrin Foundation
- **URL**: https://sovrin.org/
- **概要**: 非営利団体がガバナンスするグローバルDIDネットワーク。SSI（自己主権型アイデンティティ）の10原則を提唱
- **技術特徴**: Hyperledger Indyベースの分散型台帳。政府・企業・個人が対等にアイデンティティを管理
- **実績**: カナダBC州政府がデジタルID基盤に採用。欧州・米国で医療・金融分野での実証実験
- **適用分野**: 政府デジタルID、医療情報共有、金融KYC

#### uPort（旧Consensys）
- **URL**: https://www.uport.me/
- **概要**: Ethereum上に構築されたモバイルベースのDIDプラットフォーム
- **技術特徴**: スマートフォンアプリでEthereumベースのDIDを管理。dApps（分散型アプリケーション）とのシームレスな連携
- **実績**: スイス・ツーク市のデジタルID基盤、難民支援プログラムでのID発行
- **適用分野**: DeFi（分散型金融）、dAppsログイン、難民・無国籍者のID発行

#### ION（Identity Overlay Network）by Microsoft
- **URL**: https://identity.foundation/ion/
- **概要**: Bitcoinブロックチェーン上に構築されたレイヤー2型DIDネットワーク
- **技術特徴**: Sidetree Protocol採用。Bitcoinの不変性を活用しつつ、スケーラビリティを確保（毎秒数万件のDID操作）
- **実績**: MicrosoftがDecentralized Identity Foundationと共同開発。大規模実装に向けた技術検証完了
- **適用分野**: 大規模企業ID管理、IoTデバイス認証、グローバルサプライチェーン

## My Notes


## Rating
⭐⭐⭐⭐☆ (4/5)

**評価理由**:
- **技術成熟度**: W3C標準化完了により技術仕様は確立したが、実用化事例はまだ限定的
- **市場ポテンシャル**: プライバシー保護・GDPR対応・Web3基盤として需要は極めて高いが、法規制・ユーザー教育が課題
- **日本の取り組み**: Trusted Web構想で政府主導の推進体制が整備され、実証実験が進行中
- **課題**: 秘密鍵紛失時の復旧手段、相互運用性、ユーザー自己責任の重さ、既存システムとの統合コストが障壁

## 全体要約

Web3・分散型ID（DID）・自己主権型アイデンティティ（SSI）は、中央管理者不要で個人がアイデンティティを管理する次世代インターネット基盤である。ブロックチェーン上にID・証明書を記録し、プラットフォーム間で移動可能にすることで、GAFAM等の巨大IT企業によるデータ独占から脱却し、個人データの主権を取り戻す。

2022年にW3CがDID仕様を標準化し、VC（検証可能なクレデンシャル）と組み合わせることで、学歴・資格・医療記録等の信頼性の高い情報共有が可能になった。改ざん耐性と透明性を確保しつつ、必要最小限の情報のみを開示する選択的開示（Selective Disclosure）も実現する。

日本では内閣官房デジタル市場競争本部が2020年からTrusted Web構想を推進し、医療・サプライチェーン・人材分野で実証実験を実施。NECの金融KYCソリューション、Meta Akitaの秋田犬デジタル血統書、デジタルガレージの教育証明書発行等、実用化事例が登場している。

グローバルでは、Worldcoin（2024年10月時点で690万人登録）、Microsoft Entra Verified ID、Sovrin Foundation（カナダBC州政府採用）、uPort（スイス・ツーク市採用）、Microsoft ION等が代表的である。金融KYC/AML対応、医療情報共有、教育証明、サプライチェーン管理、難民ID発行等、適用領域は広範である。

品質保証エンジニアの視点では、秘密鍵管理のセキュリティ、ID紛失時の復旧手段、相互運用性（異なるDIDシステム間の互換性）、プライバシー保護（ゼロ知識証明、差分プライバシー）が重要課題となる。Pythonによる暗号化実装（RSA、楕円曲線暗号）、ブロックチェーン連携テスト（Ethereum、Hyperledger Indy）、セキュリティ監査が実践的スキルとして求められる。

## 日本の立ち位置・強み弱み分析

### 強み
1. **政府主導のTrusted Web構想**: 内閣官房デジタル市場競争本部が2020年から推進。産学官連携で実証実験を実施し、国際標準化への貢献も視野に入れた戦略的取り組み
2. **金融・医療での実証実験実績**: NEC、富士通等の大手IT企業が金融KYC/AML、医療情報共有でDID技術を検証。既存システムとの統合ノウハウを蓄積
3. **プライバシー保護技術の研究蓄積**: 理化学研究所、産総研、NTT研究所等でゼロ知識証明、秘密計算、差分プライバシー等の暗号技術を研究。DIDのプライバシー保護に応用可能
4. **マイナンバーカード基盤の活用可能性**: マイナンバーカードの公的個人認証サービス（JPKI）をDIDと連携させることで、政府発行の信頼できるデジタルID基盤を構築可能

### 弱み
1. **グローバルDIDプラットフォームの不在**: Microsoft Entra Verified ID、Worldcoin、Sovrin等の海外勢がデファクトスタンダード化。日本発のグローバルDIDプラットフォームが不在
2. **ブロックチェーン規制の曖昧さ**: 暗号資産規制は厳格だが、DID・NFT・DAOの法的位置づけが不明確。税制（雑所得扱い）がスタートアップ育成の障壁
3. **ユーザー教育とUI/UX未整備**: 秘密鍵管理、リカバリーフレーズ等の概念が一般ユーザーに浸透せず。使いやすいウォレットアプリ開発が遅れている
4. **相互運用性標準の遅れ**: Trusted WebとW3C DIDの関係性が曖昧。国内システム間の相互運用性すら確立しておらず、海外DIDシステムとの連携は未検証

### 取るべき戦略
- **マイナンバーカードのDID化推進**: デジタル庁がマイナンバーカードをDIDベースに拡張し、民間サービス（銀行、医療、教育）と連携可能なデジタルウォレット基盤を構築
- **Trusted WebのW3C標準化推進**: 日本が主導してTrusted WebをW3C標準に反映させ、国際的なデファクトスタンダードを獲得
- **金融・医療でのキラーユースケース創出**: マネーロンダリング対策（AML）、医療情報共有、薬剤師国家資格証明等、規制対応と利便性向上を両立する具体的サービスを早期実装
- **ユーザー教育とUI/UX改善**: 秘密鍵管理不要の社会的復旧（Social Recovery）、生体認証統合、直感的なウォレットアプリを開発し、非技術者でも使える環境を整備
- **スタートアップ支援とサンドボックス制度拡充**: DID・Web3スタートアップへの投資促進、規制サンドボックスでの実証実験を加速し、商業化スピードを向上

### 品質保証エンジニアの視点での重要ポイント

#### 秘密鍵管理とセキュリティ
- **課題**: 秘密鍵紛失時のアクセス喪失、フィッシング攻撃、マルウェアによる鍵盗難
- **対策**: 
  - 秘密鍵の安全な生成（CSPRNG：Cryptographically Secure Pseudo-Random Number Generator）
  - ハードウェアセキュリティモジュール（HSM）、セキュアエレメント（SE）への鍵保管
  - 社会的復旧（Social Recovery）：信頼できる複数人による鍵復元メカニズム
  - マルチシグ（複数署名）、閾値署名（Threshold Signature）
- **Python実装例**:
```python
from cryptography.hazmat.primitives.asymmetric import rsa, ec
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
import secrets

# RSA秘密鍵の安全な生成
def generate_rsa_keypair():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key = private_key.public_key()
    
    # PEM形式でシリアライズ
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.BestAvailableEncryption(b'strong_password')
    )
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    
    return private_pem, public_pem

# 楕円曲線暗号（ECC）秘密鍵生成（ブロックチェーン標準）
def generate_ecc_keypair():
    private_key = ec.generate_private_key(ec.SECP256K1())  # Ethereum, Bitcoin標準曲線
    public_key = private_key.public_key()
    return private_key, public_key

# デジタル署名の生成と検証
def sign_and_verify(message, private_key, public_key):
    # 署名生成
    signature = private_key.sign(
        message.encode(),
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    
    # 署名検証
    try:
        public_key.verify(
            signature,
            message.encode(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except:
        return False
```

#### ブロックチェーン連携テスト
- **課題**: Ethereum、Hyperledger Indy等の異なるブロックチェーン基盤との連携検証
- **検証項目**:
  - DIDドキュメントの書き込み・読み取り遅延
  - トランザクション失敗時のリトライロジック
  - ガス代（Gas Fee）の最適化
  - ブロックチェーンネットワークの輻輳時の挙動
- **Python実装例（Ethereumとの連携）**:
```python
from web3 import Web3
import json

# Ethereum接続
w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/YOUR_INFURA_KEY'))

# スマートコントラクトABI（例：DIDレジストリ）
contract_abi = json.loads('[...]')  # DIDレジストリのABI
contract_address = '0x...'  # デプロイ済みコントラクトアドレス

contract = w3.eth.contract(address=contract_address, abi=contract_abi)

# DIDドキュメントの登録
def register_did_on_chain(did, did_document, private_key):
    account = w3.eth.account.from_key(private_key)
    
    # トランザクション構築
    tx = contract.functions.registerDID(did, did_document).build_transaction({
        'from': account.address,
        'nonce': w3.eth.get_transaction_count(account.address),
        'gas': 200000,
        'gasPrice': w3.eth.gas_price
    })
    
    # トランザクション署名
    signed_tx = w3.eth.account.sign_transaction(tx, private_key)
    
    # トランザクション送信
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    
    # トランザクション完了待機
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    
    return tx_receipt

# DIDドキュメントの取得
def resolve_did_from_chain(did):
    did_document = contract.functions.resolveDID(did).call()
    return did_document
```

#### 相互運用性テスト
- **課題**: 異なるDIDシステム（Microsoft Entra、Sovrin、Trusted Web）間でのDID解決・VC検証
- **検証項目**:
  - DID Method（did:web, did:ethr, did:sov等）の相互変換
  - VC形式（JWT、JSON-LD）の相互互換性
  - 暗号アルゴリズム（RSA、ECDSA、EdDSA）の対応範囲
- **Python実装例**:
```python
import jwt
from datetime import datetime, timedelta

# VC（Verifiable Credential）の発行
def issue_verifiable_credential(issuer_did, subject_did, claims, private_key):
    payload = {
        '@context': ['https://www.w3.org/2018/credentials/v1'],
        'type': ['VerifiableCredential'],
        'issuer': issuer_did,
        'issuanceDate': datetime.utcnow().isoformat() + 'Z',
        'expirationDate': (datetime.utcnow() + timedelta(days=365)).isoformat() + 'Z',
        'credentialSubject': {
            'id': subject_did,
            **claims
        }
    }
    
    # JWT形式でVC生成
    vc = jwt.encode(payload, private_key, algorithm='RS256')
    return vc

# VCの検証
def verify_verifiable_credential(vc, public_key):
    try:
        payload = jwt.decode(vc, public_key, algorithms=['RS256'])
        # 有効期限チェック
        exp_date = datetime.fromisoformat(payload['expirationDate'].replace('Z', ''))
        if datetime.utcnow() > exp_date:
            return False, "Credential expired"
        return True, payload
    except jwt.ExpiredSignatureError:
        return False, "Signature expired"
    except jwt.InvalidTokenError:
        return False, "Invalid token"
```

#### プライバシー保護技術
- **課題**: 必要最小限の情報のみを開示する選択的開示（Selective Disclosure）、ゼロ知識証明
- **対策**:
  - BBS+署名（選択的開示可能な署名方式）
  - ゼロ知識証明（ZKP：Zero-Knowledge Proof）による属性証明
  - 差分プライバシー（個人特定防止）
- **Python実装例（簡易的な選択的開示）**:
```python
import hashlib
import hmac

# 選択的開示可能なクレーム構造
def create_selective_disclosure_vc(claims, private_key):
    # 各クレームをハッシュ化し、マークルツリー構造で管理
    hashed_claims = {k: hashlib.sha256(f"{k}:{v}".encode()).hexdigest() for k, v in claims.items()}
    
    # マークルルート生成
    merkle_root = hashlib.sha256(''.join(sorted(hashed_claims.values())).encode()).hexdigest()
    
    # VCに含めるのはマークルルートのみ
    vc = {
        'merkleRoot': merkle_root,
        'hashed_claims': hashed_claims
    }
    
    # デジタル署名
    signature = hmac.new(private_key.encode(), merkle_root.encode(), hashlib.sha256).hexdigest()
    vc['signature'] = signature
    
    return vc, claims  # 実際のクレームは保有者が保管

# 特定クレームのみを開示
def disclose_claim(vc, claim_key, claim_value, original_claims):
    # クレームのハッシュを再計算
    claim_hash = hashlib.sha256(f"{claim_key}:{claim_value}".encode()).hexdigest()
    
    # VCに含まれるハッシュと一致するか検証
    if vc['hashed_claims'].get(claim_key) == claim_hash:
        return True, {claim_key: claim_value}
    else:
        return False, None
```

#### セキュリティ監査
- **監査項目**:
  - OWASP Top 10（Webアプリケーションセキュリティ）準拠
  - ISO/IEC 27001（情報セキュリティマネジメント）準拠
  - GDPR、個人情報保護法対応
  - ペネトレーションテスト（侵入テスト）
  - スマートコントラクト監査（Solidity）
- **Python実装例（セキュリティ自動テスト）**:
```python
import requests
from bs4 import BeautifulSoup

# SQLインジェクション脆弱性チェック
def test_sql_injection(url):
    payloads = ["' OR '1'='1", "1; DROP TABLE users--", "' UNION SELECT NULL--"]
    vulnerable = False
    
    for payload in payloads:
        response = requests.get(f"{url}?id={payload}")
        if "error" not in response.text.lower() and response.status_code == 200:
            vulnerable = True
            print(f"[WARNING] Potential SQL injection: {payload}")
    
    return vulnerable

# XSS（クロスサイトスクリプティング）脆弱性チェック
def test_xss(url):
    payloads = ["<script>alert('XSS')</script>", "<img src=x onerror=alert('XSS')>"]
    vulnerable = False
    
    for payload in payloads:
        response = requests.get(f"{url}?input={payload}")
        if payload in response.text:
            vulnerable = True
            print(f"[WARNING] Potential XSS: {payload}")
    
    return vulnerable

# セキュリティヘッダーチェック
def check_security_headers(url):
    response = requests.get(url)
    headers = response.headers
    
    required_headers = [
        'X-Content-Type-Options',
        'X-Frame-Options',
        'Strict-Transport-Security',
        'Content-Security-Policy'
    ]
    
    missing_headers = [h for h in required_headers if h not in headers]
    
    if missing_headers:
        print(f"[WARNING] Missing security headers: {missing_headers}")
    
    return len(missing_headers) == 0
```

### 実務適用のポイント
1. **段階的実装**: 
   - Phase 1: 社内従業員ID管理でDID/VCを導入し、技術検証
   - Phase 2: 取引先・パートナー企業との相互認証に拡大
   - Phase 3: 顧客向けデジタルウォレット提供、B2Cサービス展開

2. **既存システムとの統合**:
   - LDAP（Lightweight Directory Access Protocol）、SAML（Security Assertion Markup Language）との連携
   - OAuth 2.0、OpenID Connectとの相互運用性確保
   - レガシーシステムとのハイブリッド運用期間を設定

3. **ユーザー教育とサポート**:
   - 秘密鍵管理のトレーニング（リカバリーフレーズのバックアップ方法）
   - フィッシング対策教育（偽サイト・偽アプリへの警戒）
   - 24時間サポート体制構築（紛失・盗難時の緊急対応）

4. **コンプライアンス対応**:
   - GDPR（EU一般データ保護規則）：「忘れられる権利」「データポータビリティ」への対応
   - 個人情報保護法：第三者提供記録、安全管理措置の実施
   - 金融規制（AML/CFT）：マネーロンダリング・テロ資金供与対策

---

**関連技術**:
- [[T8-01-03_Blockchain_NFT_Economy]] - ブロックチェーン・NFT経済圏基盤
- [[T1-01-01_Urban_Integrated_Data_Platform]] - 都市統合データプラットフォーム
- [[T8-07-04_Metaverse_Economy]] - メタバース経済・バーチャル労働市場
