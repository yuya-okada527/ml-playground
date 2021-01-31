# Movie Recommender API

Movie Recommender App 用のコア API を提供します。

## 使用技術

- 言語: Python3.8
- フレームワーク: FastAPI
- サーバ: uvicorn
- ミドルウェア: Apache Solr, Redis
- 主要ライブラリ
  - requests
  - pydantic
  - redis-py

## 起動方法

```bash
# ローカル起動
$ uvicorn app.main:app --reload
```
