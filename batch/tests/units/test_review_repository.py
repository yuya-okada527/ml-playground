from domain.models.internal.movie_model import Review
from infra.repository.input.review_repository import ReviewRepository
from sqlalchemy.engine.base import Connection, Engine


def test_fetch_all_review_id(conn: Connection):

    # テストデータ
    review = Review(review_id="review_id", movie_id=0, review="review")
    conn.execute("INSERT INTO reviews VALUES (?, ?, ?)",
        review.review_id,
        review.movie_id,
        review.review
    )

    # テスト用のリポジトリを初期化
    review_repository = ReviewRepository(conn)

    assert review_repository.fetch_all_review_id() == [review.review_id]
