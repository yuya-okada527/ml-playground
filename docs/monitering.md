# 監視・分析基盤に関して

## 欲しい機能

- アクセス解析
  - Google Analitics を検討
- ログ監視・検索
  - error/warn ログの検知
    - Cloud Error Reporting を利用
  - ログの検索
    - オンラインは、Cloud Logging をしばらく使ってみる
  - ステータスコードの監視
    - Cloud Monitoring
  - レスポンスタイムの監視
    - Cloud Monitoring
- リソース監視
  - CPU 使用率
  - メモリ使用量
  - ディスク使用量
  - ダッシュボードを作成
- 死活監視
  - Cloud Monitoring Uptime Check

## SLO

- Core API
  - ステータスコード 200 率
  - レスポンスタイム
    - Metric: loadbalancing.googleapis.com/https/total_latencies
    - SLI: Less Than 500 ms
    - SLO: 99%
  - 可用性
    - Cloud Monitoring Uptime Check
