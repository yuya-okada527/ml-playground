# スケーラビリティ

## リクエスト数に対するスケーラビリティ

### フロントエンド

- Next.js を利用し、機能の一部を SSG で構築
- Vercel を利用し、グローバル CDN で配信を行う

### バックエンド

- Kubenetes 上にワークロードを作成し、容易にスケール可能な構成を実現
- 機械学習による推論は、バッチ処理で事前実行したものを Redis 上に格納し、 オンライン推論の負荷を軽減
- バックエンドとして、Apache Solr と redis を採用、分散クラスタを構築可能

## データ数に対するスケーラビリティ

### バックエンド

- 機械学習推論部分では、Annoy(近似最近傍探索)を利用、実直な方法に比べ、大幅に計算効率を改善
