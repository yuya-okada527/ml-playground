# Movie Recommender Batch

Movie Recommender App 用のバッチ処理を提供します。

## 使用技術

- 言語: Python3.9
- フレームワーク: typer
- ORM: sqlalchemy(ORM 部分は未使用)
- ミドルウェア: MySQL, Apache Solr, Redis
- 主要ライブラリ:
  - requests
  - pydantic
  - redis-py

## 起動方法

```bash
# ローカル起動(Help)
$ python app/main.py --help
# 入稿処理
$ sh shells/exec_input.sh
# 出稿処理
$ sh shells/exec_output.sh
# 類似映画データ作成処理
$ sh shells/exec_similarity.sh
```

## 静的解析

```bash
# flake8(1行の文字数制限とビジュアルインデントは無視)
flake8 app --ignore E501,E128
```
