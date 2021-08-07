# ML Playground App

機械学習を利用したアプリのデモ環境を提供します。<br>
本リポジトリでは、ドキュメントとローカル開発用の docker-compose ファイルを管理する。

- 本番環境: https://ml-playground-fe.vercel.app/

## コンセプト

機械学習を実社会におけるサービスで運用・改善できるシステムを構築する。<br>
そのために下記の 5 つの指標を重視し、改善していきます。

- [スケーラビリティ](https://github.com/yuya-okada527/ml-playground/blob/develop/docs/phase1/scalability.md)
- [オブザーバビリティ](https://github.com/yuya-okada527/ml-playground/blob/develop/docs/phase1/obserbability.md)
- [継続的改善性](https://github.com/yuya-okada527/ml-playground/blob/develop/docs/phase1/continuous_improvements.md)
- コストパフォーマンス
- エンド to エンドの評価

## 全体構成

![全体構成](https://github.com/yuya-okada527/ml-playground/blob/develop/docs/migration/images/AS_IS.png)

現在、[プラットフォームの移行を検討中](https://github.com/yuya-okada527/ml-playground/blob/develop/docs/migration/migration.md)

## データ分析パイプライン

![データ分析パイプライン](https://github.com/yuya-okada527/ml-playground/blob/develop/docs/phase2/images/data_pipeline_design.png)

## コンポーネント (詳細は各コンポーネントの README を参照)

- [FE](https://github.com/yuya-okada527/ml-playground-fe)
  - フロントエンドアプリ
- [Core API](https://github.com/yuya-okada527/ml-playground-core-api)
  - コア機能 API
- [Batch](https://github.com/yuya-okada527/ml-playground-batch)
  - Batch 処理(データの作成とフィード処理を担う)
- [Log ETL](https://github.com/yuya-okada527/ml-playground-stream)
  - Log ETL 処理

## 使用技術概要 (詳細は各コンポーネントの README を参照)

- プラットフォーム:
  - GCP (バックエンドで利用)
    - Cloud Functions
  - Vercel (フロントエンドで利用)
  - Kubernetes (GKE Autopilot)
- ミドルウェア
  - MySQL (Cloud SQL)
  - Apache Solr (フェーズ 1 のみ)
  - Redis (フェーズ 1 のみ)
  - Cloud Pub/Sub
  - Cloud Storage
  - BigQuery
- 言語:
  - Python (3.8, 3.9)
  - Node.js (v14)
  - TypeScript (4.0)
- フレームワーク / ライブラリ
  - バックエンド:
    - FastAPI (Web フレームワーク)
    - Typer (バッチアプリ フレームワーク) (フェーズ 1 のみ)
    - SQLAlchemy
    - Serverless Framework
  - フロントエンド:
    - React.js
    - Next.js
    - Material-UI (コンポーネントライブラリ)
  - 機械学習:
    - kedro (ワークフロー管理)
    - mlflow tracking (実験管理)
    - spaCy (自然言語処理)
    - Annoy (近似最近傍探索)
- CI/CD
  - Github Actions (CI パイプライン)
- テスティングライブラリ
  - pytest (バックエンドの Unit テストで利用)
  - jest (フロントエンドの Unit テストで利用)
  - Cypress (API の E2E で利用)
  - Playwright (フロントエンドの E2E で利用)

## 関連リポジトリ

- [FE E2E](https://github.com/yuya-okada527/ml-playground-fe-e2e)
