# 移行計画

現在、下記のアーキテクチャ上の問題を解決するために、プラットフォームの移行を準備中です。

## 現在の問題点

- 問題: オンラインで運用している、検索サーバ(Solr)、KVS(Redis)、API のコストが大きい。
  - 解決: 時間課金のプラットフォームから、リクエスト数による課金プラットフォームに移行する
- 問題: 検索サーバの可用性に不安がある
  - 解決: 安定した SaaS 系プロダクトである Algolia へ移行する

## 現在のアーキテクチャ

![現在](https://github.com/yuya-okada527/ml-playground/blob/develop/docs/migration/images/AS_IS.png)

## 移行後のアーキテクチャ

![移行後](https://github.com/yuya-okada527/ml-playground/blob/develop/docs/phase2/images/phase2.png)
