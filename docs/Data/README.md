# データ設計

## 入稿 DB

![入稿DB](https://github.com/yuya-okada527/movie-recommender/blob/main/docs/Data/ER%E5%9B%B3.png)

## Solr Schema

![スキーマ](https://github.com/yuya-okada527/movie-recommender/blob/main/docs/Data/solr-schema.png)

### フリーワード

以下の項目をスペース区切り

- OriginalTitle
- JapaneseTitle
- GenreLabels をスペース区切り
- KeywordLabels をスペース区切り

### schema API

参照: https://github.com/yuya-okada527/movie-recommender/blob/main/batch/resources/solr/schema.json

### index_time

バージョニングに使用

## 類似性 KVS

### データ構造

下記構造で、映画 ID に紐づく類似映画 ID の上位 5 つをもつ

- Key: {Model 名}\_{movie_id}
- Value: movie_id の配列(サイズ=5)
