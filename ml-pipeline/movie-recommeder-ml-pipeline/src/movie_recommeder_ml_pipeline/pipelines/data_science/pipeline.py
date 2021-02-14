from kedro.pipeline import node, Pipeline
from movie_recommeder_ml_pipeline.pipelines.data_science.nodes import (
    predict_similar_movies
)


def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                func=predict_similar_movies,
                inputs=["review_vectors", "parameters"],
                outputs="similar_movies",
                name="predict_similar_movies"
            )
        ]
    )
