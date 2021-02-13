from typing import Protocol
from domain.models.internal.movie import Review

from infra.repository.input.base import ENGINE


# ---------------------------
# SQL
# ---------------------------
SELECT_ALL_REVIEW_ID_STATEMENT = """\
SELECT
    review_id
FROM
    reviews
"""
INSERT_REVIEW_STATEMENT = """\
INSERT INTO
    reviews
VALUES
    (
        %(review_id)s,
        %(movie_id)s,
        %(review)s
    )
"""

# TODO Protocolよりabcの方が使いやすい？
class AbstractReviewRepository(Protocol):

    def fetch_all_review_id(self) -> list[str]:
        ...
    
    def save_review_list(self, review_list: list[Review]) -> int:
        ...


class ReviewRepository:

    def fetch_all_review_id(self) -> list[str]:
        
        # SQL実行
        result_proxy = ENGINE.execute(SELECT_ALL_REVIEW_ID_STATEMENT)

        return [int(review.review_id) for review in result_proxy]
    
    def save_review_list(self, review_list: list[Review]) -> int:
        
        count = 0
        # トランザクション開始
        with ENGINE.begin() as conn:
            for review in review_list:
                count += conn.execute(INSERT_REVIEW_STATEMENT, {
                    "review_id": review.review_id,
                    "movie_id": review.movie_id,
                    "review": review.review
                }).rowcount
        
        return count
