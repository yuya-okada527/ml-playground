from typing import Dict
import pandas as pd
from annoy import AnnoyIndex



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
