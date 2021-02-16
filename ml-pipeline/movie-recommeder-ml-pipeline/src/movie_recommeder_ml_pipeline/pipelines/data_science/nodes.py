import os
from typing import Dict
from pathlib import Path

import pandas as pd
from annoy import AnnoyIndex
import mlflow


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
    vector_size = review_vectors["vector"][0].size
    annoy_index = AnnoyIndex(vector_size, parameters["similarity_metrics"])
    annoy_index.set_seed(parameters["random_seed"])

    # インデックスの構築
    idx2movie = {}
    for i, row in enumerate(review_vectors.itertuples()):
        idx2movie[i] = row.movie_id
        annoy_index.add_item(i, row.vector)
    annoy_index.build(parameters["n_tree"])

    # 類似映画トップNを予測
    similar_movies = {}
    for j in range(len(review_vectors)):
        # 同じ映画が最も近くなるため、1つずらす
        similar_movies[idx2movie[j]] = annoy_index.get_nns_by_item(j, parameters["predict_num"] + 1)[1:]

    return pd.DataFrame({
        "movie_id": similar_movies.keys(),
        "similar_movie_ids": similar_movies.values()
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
            "similar_movie_list": similar_movie_list
        })

        # 類似映画が5件だけのものに絞る
        test_data = test_data[test_data.apply(lambda x: len(x["similar_movie_list"]), axis=1) == 5]

        mlflow.log_metric("test_size", len(test_data))

    return test_data
