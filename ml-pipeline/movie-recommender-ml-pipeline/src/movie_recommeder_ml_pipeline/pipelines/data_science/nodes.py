import os
from typing import Dict
from pathlib import Path

import redis
import mlflow
import pandas as pd
from annoy import AnnoyIndex
from pandas.io import json


# mlflowログ出力ディレクトリ
MLFLOW_PATH = os.path.join(
    Path(__file__).resolve().parents[5],
    "mlruns"
)


def predict_similar_movies(
    review_vectors: pd.DataFrame,
    parameters: Dict
) -> pd.DataFrame:

    # 近似最近傍探索モデルを初期化
    vector_size = review_vectors.iat[0, 1].size
    annoy_index = AnnoyIndex(vector_size, parameters["similarity_metrics"])
    annoy_index.set_seed(parameters["random_seed"])

    # TODO ログ
    print(f"review size: {len(review_vectors)}")

    # インデックスの構築
    idx2movie = {}
    for i, row in enumerate(review_vectors.itertuples()):
        idx2movie[i] = row.movie_id
        annoy_index.add_item(i, row.vector)

        # TODO ログ
        if i % 10 == 0:
            print(f"{i}番目のインデックスを構築完了")
    annoy_index.build(parameters["n_tree"])

    # 類似映画トップNを予測
    similar_movies = {}
    for j in range(len(review_vectors)):
        # 同じ映画が最も近くなるため、1つずらす
        similar_movies[idx2movie[j]] = annoy_index.get_nns_by_item(j, parameters["predict_num"] + 1)[1:]

        if j % 10 == 0:
            print(f"{j}番目の推論完了")

    return pd.DataFrame({
        "movie_id": similar_movies.keys(),
        "similar_movie_ids": [[idx2movie[movie_id] for movie_id in movie_list] for movie_list in similar_movies.values()]
    })


def make_test_data(tmdb_similar_movies: pd.DataFrame) -> pd.DataFrame:

    # mlflow用のログディレクトリを準備
    # mlflow.set_tracking_uri(f"file:/{MLFLOW_PATH}")
    mlflow.set_experiment("make_test_data")

    # 実験開始
    with mlflow.start_run():
        # 映画IDごとに類似映画を集約して5件以下に絞る
        similar_movie_list = (tmdb_similar_movies.groupby("movie_id")["similar_movie_id"]
            .apply(list)
            .apply(lambda x: x[:5])
        )

        # テストデータを構築
        test_data = pd.DataFrame({
            "movie_id": similar_movie_list.index,
            "test_similar_movie_ids": similar_movie_list
        })

        # 類似映画が5件だけのものに絞る
        test_data = test_data[test_data.apply(lambda x: len(x["test_similar_movie_ids"]), axis=1) == 5]

        mlflow.log_metric("test_size", len(test_data))

    return test_data


def evaluate_results(
    similar_movies: pd.DataFrame,
    test_data: pd.DataFrame
) -> pd.DataFrame:

    mlflow.set_experiment("evaludate_results")

    with mlflow.start_run():

        # 推論結果とテストデータをマージする
        data = pd.merge(similar_movies, test_data)

        # 比較対象の類似映画IDリスト文字列をセットに変換
        data["similar_movie_ids"] = data["similar_movie_ids"].apply(json.loads).apply(set)
        data["test_similar_movie_ids"] = data["test_similar_movie_ids"].apply(json.loads).apply(set)

        # 両方に存在するIDの数を数える
        data["match_num"] = data.apply(lambda x: len(x["similar_movie_ids"] & x["test_similar_movie_ids"]), axis=1)

        # 正解率を計算
        data_size = len(data)
        accuracy = sum(data["match_num"] / (data_size * 5))

        mlflow.log_metric("data_size", data_size)
        mlflow.log_metric("accuracy", accuracy)


def feed_similar_movies(
    similar_movies: pd.DataFrame,
    parameters: Dict
) -> pd.DataFrame:

    redis_client = redis.Redis(host=os.environ.get("REDIS_HOST", "localhost"), port=6379)

    for row in similar_movies.itertuples():
        # モデルキー名
        key = f"{row.movie_id}_{parameters['model_name']}"

        redis_client.set(key, json.dumps(row.similar_movie_ids))
