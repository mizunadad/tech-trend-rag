---
title: "JS6.4 Infrastructure Disaster Recovery - インフラ災害復旧"
url: 
  - https://www.gartner.com/en/documents/5142308
  - https://aws.amazon.com/disaster-recovery/
  - https://cloud.google.com/architecture/disaster-recovery
date: 2025-10-15
tags:
  - Gartner2025
  - Infrastructure
  - DisasterRecovery
  - BusinessContinuity
  - Resilience
  - 品質保証
  - BCP
rating: ⭐⭐⭐⭐⭐
---

# JS6.4 Infrastructure Disaster Recovery - インフラ災害復旧

## 📊 ハイプ・サイクル位置情報

**ハイプサイクル位置:** 📊 Slope of Enlightenment（啓発の坂道）  
**実用化時期:** 🔵 2-5年で実用化  
**日本の立ち位置:** 🟢 強み分野  
**カテゴリー:** JS6 セキュリティ・レジリエンス分野

## 🎯 5つの要点サマリー

### 1. **定義と基本概念**
Infrastructure Disaster Recovery（インフラDR）は、**自然災害・サイバー攻撃・人的ミス等によりITインフラが被災した際、迅速に復旧し事業継続を確保する包括的戦略**。従来のバックアップ中心の考え方から、以下の4つの指標を中心とした設計へ進化:
- **RPO（Recovery Point Objective: 目標復旧時点）**: どの時点までデータを復元するか（例: 15分前のデータまで復旧）
- **RTO（Recovery Time Objective: 目標復旧時間）**: どれだけ早くシステムを復旧させるか（例: 1時間以内に復旧）
- **RTA（Recovery Time Actual: 実際の復旧時間）**: 実際にかかった復旧時間。RTOとのギャップを分析
- **MTD（Maximum Tolerable Downtime: 最大許容停止時間）**: 事業継続上、許容できる最大停止時間

クラウド時代のDRは、**Multi-Region構成**（地理的に離れた複数リージョンにシステム配置）、**自動フェイルオーバー**（障害時に自動で待機系へ切替）、**定期的なDRテスト**（年2回以上のリハーサル実施）が標準となっている。

### 2. **ICテスト・品質保証分野への影響**
- **テストデータの保護**: ウェーハマップ、不良解析データ等の重要品質データを地理的に離れた場所にリアルタイムレプリケーション。データ消失リスク最小化
- **テスト環境の迅速復旧**: 地震・火災等でテスト装置が被災しても、クラウドDR環境で代替テスト実行。製品出荷遅延を回避
- **サプライチェーン連携の継続性**: ファウンドリ・テストハウスとのデータ連携が途絶えても、DR環境で継続。グローバルサプライチェーンの信頼性向上
- **ランサムウェア対策**: 暗号化攻撃を受けても、隔離されたバックアップから迅速復旧。身代金支払いを回避
- **規制対応**: 個人情報保護法、GDPR等でBCP（Business Continuity Plan）策定が義務化。DR体制整備は必須要件

### 3. **実装課題と技術的要件**
- **コストとRPO/RTOのトレードオフ**: RPO=0（データ消失ゼロ）、RTO=0（即座復旧）は理想だが、実現にはActive-Active構成（常時2拠点稼働）が必要でコスト高
- **DR戦略の選択**: 
  - **Backup & Restore**: 最も安価だが、RTO/RPOが長い（数時間～数日）
  - **Pilot Light**: 最小限のDR環境を常時起動。RTO=数時間、中コスト
  - **Warm Standby**: DR環境を縮小版で常時稼働。RTO=数十分、中～高コスト
  - **Active-Active**: 本番・DR両環境を常時フル稼働。RTO=数秒、最高コスト
- **データ整合性の確保**: 非同期レプリケーション時、障害発生タイミングによりデータ不整合が発生するリスク。トランザクション整合性設計が必要
- **DR訓練の形骸化**: 年1回のDRテストが形式的になり、実際の障害時に機能しない事例多数。**Chaos Engineering**的な抜き打ちDRテストが有効
- **クラウドDRの落とし穴**: オンプレミス→クラウドDR移行時、ネットワーク帯域不足でRTO目標未達成のリスク。事前の帯域計算・確保が必須

### 4. **日本の状況と強み**
- **災害大国としての意識の高さ**: 阪神・淡路大震災（1995年）、東日本大震災（2011年）、熊本地震（2016年）等、大規模災害を経験。BCP/DR体制は**世界トップレベル**
- **金融業界の先行**: 金融庁の「金融機関等におけるシステムリスク管理態勢の確認検査マニュアル」により、銀行・証券はDR体制整備が義務化。三菱UFJ、みずほ等は東西2拠点のActive-Active構成を運用
- **製造業の高水準**: トヨタは東日本大震災後、グローバル全工場の生産データをリアルタイムバックアップ。1拠点被災しても他拠点で生産継続可能
- **クラウドDR活用の加速**: AWS、Azure、Google Cloudの日本リージョン拡充（東京・大阪・名古屋等）により、低コストでMulti-Region DR構成が可能に

### 5. **品質保証エンジニアとしての推奨アクション**
- **フェーズ1（3ヶ月）**: BIA（Business Impact Analysis）実施。テスト装置・データの重要度を評価し、RPO/RTO目標を設定
- **フェーズ2（6ヶ月）**: バックアップ戦略見直し。オンプレミステープバックアップから、クラウドバックアップ（AWS Backup、Azure Backup）へ移行
- **フェーズ3（1年）**: Pilot Light DR環境構築。テストデータベース・解析サーバーのDR環境をクラウドに構築（縮小版で常時起動）
- **フェーズ4（1.5年）**: DR訓練の実施。四半期ごとにDRサイトへのフェイルオーバー訓練。RTO目標達成を検証
- **フェーズ5（2-3年）**: Active-Active構成へ移行。重要テストシステムは東京・大阪2リージョンで常時稼働。障害時も無停止

---

## 🏢 具体的プロダクト事例

### 日本企業の先進事例

#### **トヨタ自動車 - グローバル生産ネットワークのBCP/DR**
- **導入背景**: 東日本大震災（2011年）でサプライチェーン寸断。部品供給停止により、グローバル全工場が数週間停止
- **実装内容**:
  - **RESCUEⅡ**: トヨタ独自のBCPシステム。グローバル約50,000社のサプライヤー情報をデータベース化
  - **Multi-Region DR**: 生産データ（設計図、製造指示、品質データ）を日本・米国・欧州の3拠点でリアルタイムレプリケーション
  - **自動フェイルオーバー**: 1拠点被災時、30分以内に他拠点へ自動切替
  - **四半期DR訓練**: 全グローバル拠点で定期的にDR訓練実施。2011年の教訓を風化させない
- **成果**: 熊本地震（2016年）では、被災工場の生産を他工場へ即座に振り分け。生産停止を**最小化**
- **参考**: [トヨタ BCP取り組み（日本語）](https://global.toyota/jp/sustainability/esg/challenge2050/challenge6/)

#### **みずほ銀行 - 金融システムのActive-Active DR**
- **導入背景**: 金融庁の厳格な規制要求。システム障害時のRTO=2時間以内が必須
- **実装内容**:
  - **東西2センター**: 東京・大阪の2データセンターでActive-Active構成
  - **同期レプリケーション**: 勘定系データを両センター間でリアルタイム同期。RPO=0（データ消失ゼロ）
  - **DNS自動切替**: 障害時、DNS（Domain Name System）を自動更新し、ユーザーを正常センターへ誘導
  - **月次DR訓練**: 毎月、深夜時間帯にフェイルオーバー訓練実施
- **成果**: 2019年のシステム障害時、2時間以内に復旧。金融庁の要求基準を満たす
- **参考**: [みずほ銀行 システム安定化計画](https://www.mizuhobank.co.jp/corporate/information/system/)

#### **日立製作所 - Lumada IoT基盤のDR**
- **導入背景**: 顧客企業（製造業、鉄道等）のミッションクリティカルデータを預かるため、高可用性が必須
- **実装内容**:
  - **Multi-Cloud DR**: AWS、Azure、Google Cloudの3社を併用。1社障害時も継続
  - **Kubernetes自動復旧**: コンテナ障害時、30秒以内に自動再起動
  - **定期バックアップ**: 顧客データを6時間ごとにバックアップ。RPO=6時間
- **成果**: 稼働率99.9%以上を達成。顧客からの信頼獲得
- **参考**: [日立Lumada 可用性保証](https://www.hitachi.co.jp/products/it/lumada/)

#### **NTTデータ - データセンター相互バックアップ**
- **導入背景**: 顧客企業のシステム運用受託において、DR体制が契約必須要件
- **実装内容**:
  - **三鷹・堂島2拠点**: 東京三鷹と大阪堂島の2データセンターで相互バックアップ
  - **L7負荷分散**: アプリケーションレイヤーで負荷分散。障害時も無停止
  - **年2回DR訓練**: 全顧客システムで年2回、本番環境でのDR訓練実施
- **成果**: 顧客システムでRTO=1時間以内を保証。大手企業からの受注増加
- **参考**: [NTTデータ BCP/DRソリューション](https://www.nttdata.com/jp/ja/services/bcp-dr/)

---

### グローバルスタンダード

#### **AWS - Disaster Recovery Solutions**
- **概要**: AWSが提供する包括的なDRソリューション群
- **特徴**:
  - **AWS Backup**: 自動バックアップサービス。EC2、RDS、EFS等を統合管理
  - **AWS Elastic Disaster Recovery (CloudEndure)**: オンプレミス→AWS自動レプリケーション。RTO=数分
  - **Multi-Region**: 世界33リージョン。地理的に離れた拠点へ自動レプリケーション
  - **Pilot Light/Warm Standby テンプレート**: DR構成のベストプラクティスをテンプレート提供
- **導入企業**: Netflix、Airbnb、Samsung等がMulti-Region DR構成を採用
- **参考**: [AWS Disaster Recovery](https://aws.amazon.com/disaster-recovery/)

#### **Microsoft Azure - Site Recovery**
- **概要**: Azure Site Recoveryによる自動DR環境構築
- **特徴**:
  - **オンプレ→Azure自動レプリケーション**: VMware、Hyper-V、物理サーバーをAzureへ自動複製
  - **Azure-to-Azure DR**: Azure内で別リージョンへ自動レプリケーション
  - **1クリックフェイルオーバー**: 管理画面から1クリックでDRサイトへ切替
  - **RPO=30秒**: 継続的レプリケーションによりデータ消失を最小化
- **導入企業**: BMW、HP、Adobe等
- **参考**: [Azure Site Recovery](https://azure.microsoft.com/en-us/products/site-recovery/)

#### **Google Cloud - Disaster Recovery Planning Guide**
- **概要**: Google Cloudの包括的DRガイドとソリューション
- **特徴**:
  - **Multi-Region設計**: 世界40リージョンで地理的冗長性確保
  - **Persistent Disk Snapshot**: ディスクスナップショットを別リージョンへ自動バックアップ
  - **Cloud SQL High Availability**: データベースの自動フェイルオーバー
  - **Terraform DR自動化**: インフラをコード化し、DR環境を自動構築
- **導入企業**: Spotify、Twitter、Snap等
- **参考**: [Google Cloud DR Planning](https://cloud.google.com/architecture/dr-scenarios-planning-guide)

#### **VMware - Site Recovery Manager (SRM)**
- **概要**: VMware環境の自動DR・フェイルオーバー製品
- **特徴**:
  - **自動化オーケストレーション**: 数百台のVMを正しい順序で自動起動
  - **無停止テスト**: 本番環境に影響を与えず、DR環境でテスト実行
  - **vSphere統合**: VMware仮想化基盤とシームレス統合
  - **RTO=数分**: 自動化により手動作業を排除
- **導入企業**: Fortune 500の80%以上がVMware採用（VMware公表）
- **参考**: [VMware Site Recovery Manager](https://www.vmware.com/products/site-recovery-manager.html)

#### **Veeam - Backup & Replication**
- **概要**: 仮想化・クラウド環境のバックアップ専門製品
- **特徴**:
  - **3-2-1ルール**: 3コピー、2種類メディア、1オフサイトの自動化
  - **Instant VM Recovery**: バックアップから数分でVM起動。RTO最小化
  - **Cloud Tier**: バックアップデータをAWS S3、Azure Blob等へ自動転送
  - **Ransomware対策**: 不変（Immutable）バックアップで暗号化攻撃防御
- **導入企業**: 45万社以上が採用（Veeam公表）
- **参考**: [Veeam Backup & Replication](https://www.veeam.com/vm-backup-recovery-replication-software.html)

#### **Zerto - Continuous Data Protection (CDP)**
- **概要**: 継続的データ保護に特化したDR製品
- **特徴**:
  - **RPO=数秒**: I/Oレベルでリアルタイムレプリケーション
  - **任意時点復旧**: 過去任意の時点（数秒単位）へロールバック可能
  - **Long Distance Replication**: WAN経由で数千km離れた拠点へレプリケーション
  - **Non-Disruptive Testing**: 本番影響ゼロでDRテスト実行
- **導入企業**: GE、Coca-Cola、Credit Suisse等
- **参考**: [Zerto Platform](https://www.zerto.com/)

---

## 💡 My Notes

（ここに個人的な気づき、アクションアイテム、関連リンク等を記載）

---

## ⭐ Rating: 5/5

**評価理由:**
- **重要性**: 自然災害・サイバー攻撃の脅威が増大する中、BCP/DR体制は事業継続の生命線
- **日本の強み**: 災害大国として、BCP/DR意識は世界トップレベル。東日本大震災の教訓が組織に浸透
- **実装可能性**: クラウドDR（AWS、Azure、Google Cloud）により、低コストでMulti-Region構成が実現可能
- **品質保証への影響**: テストデータ保護、テスト環境の迅速復旧により、製品出荷遅延リスクを最小化
- **ROI**: トヨタの事例では、BCP投資により熊本地震時の生産停止を最小化。事業損失を数百億円規模で回避

**満点評価の理由:**
日本企業にとって、実装が進んでおり更なる高度化が期待できる分野。災害経験を活かした独自の強みがある。

---

## 📝 全体要約の特徴（5つの要点）

### 1. **RPO/RTOによる定量的DR設計**
従来の「バックアップさえあれば安心」という曖昧な考え方から、**RPO（目標復旧時点）・RTO（目標復旧時間）を定量的に設定**し、それを達成するアーキテクチャを設計。金融業界ではRPO=0（データ消失ゼロ）、RTO=2時間以内が標準。製造業でも、基幹システムはRPO=15分、RTO=1時間が求められるようになっている。

### 2. **クラウドがDRを民主化**
従来のDRは、地理的に離れた2拠点にデータセンターを構築する必要があり、**数億円規模の投資**が必要だった。クラウド時代は、AWS、Azure、Google CloudのMulti-Region機能により、**月額数十万円でDR環境構築が可能**。中小企業でも高水準のDR体制を実現できるようになった。

### 3. **自動化がDRの成否を分ける**
障害発生時、人間が手動でDRサイトへ切り替えると、パニック・手順ミス等で**RTO目標を大幅超過**するリスク。AWS Elastic Disaster Recovery、Azure Site Recovery等の自動フェイルオーバー機能により、**数分でDR完了**。自動化により、深夜・休日の障害でも即座に対応可能。

### 4. **DR訓練の重要性 - "訓練なきDRは絵に描いた餅"**
DR環境を構築しても、定期的な訓練がなければ実際の障害時に機能しない。金融業界では**年2回以上のDR訓練が義務化**されているが、製造業では年1回すら実施していない企業も多い。Netflix、Googleは**Chaos Engineering的な抜き打ちDRテスト**を実施し、常に実戦準備を維持。日本企業も、形式的な訓練から実践的訓練へ転換が必要。

### 5. **ランサムウェア対策としてのDR**
近年、ランサムウェア攻撃（データを暗号化し身代金要求）が急増。バックアップも暗号化されると復旧不可能に。対策として、**不変（Immutable）バックアップ**（一度書き込んだら削除・変更不可）と、**オフラインバックアップ**（ネットワーク切断）が重要。Veeam、AWS Backupはこれらの機能を標準装備。DR体制は、災害対策だけでなくサイバー攻撃対策としても必須。

---

## 🇯