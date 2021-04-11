from kedro.pipeline import node, Pipeline
from movie_recommeder_ml_pipeline.pipelines.data_science.nodes import (
    make_test_data, predict_similar_movies, feed_similar_movies
)


def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                func=predict_similar_movies,
                inputs=["review_vectors", "parameters"],
                outputs="similar_movies",
                name="predict_similar_movies"
            ),
            node(
                func=make_test_data,
                inputs="tmdb_similar_movies",
                outputs="test_data",
                name="make_test_data"
            ),
            # node(
            #     func=evaluate_results,
            #     inputs=["similar_movies", "test_data"],
            #     outputs=None,
            #     name="evaluate_results"
            # ),
            node(
                func=feed_similar_movies,
                inputs=["similar_movies", "parameters"],
                outputs=None,
                name="feed_similar_movies"
            )
        ]
    )
