from kedro.pipeline import node, Pipeline
from movie_recommeder_ml_pipeline.pipelines.data_engineering.nodes import (
    concatenate_reviews,
    normalize_reviews,
    vectorize_reviews
)


def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                func=concatenate_reviews,
                inputs="reviews",
                outputs="concatenated_reviews",
                name="concatenate_reviews"
            ),
            node(
                func=normalize_reviews,
                inputs="concatenated_reviews",
                outputs="normalized_reviews",
                name="normalize_reviews"
            ),
            node(
                func=vectorize_reviews,
                inputs=["normalized_reviews", "parameters"],
                outputs="review_vectors",
                name="vectorize_reviews"
            )
        ]
    )
