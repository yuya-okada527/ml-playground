"""レビューリポジトリモジュール

レビューテーブルに対するアクセス機能を提供するモジュール
"""
from typing import Protocol

from core.logger import create_logger
from domain.models.internal.movie_model import Review
from infra.repository.input.base_repository import ENGINE
from sqlalchemy.engine.base import Engine
from sqlalchemy.exc import DataError, IntegrityError

log = create_logger(__file__)

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
        """全てのレビューIDを取得する"""
        ...

    def save_review_list(self, review_list: list[Review]) -> int:
        """レビューデータを保存する"""
        ...


class ReviewRepository:

    def __init__(self, engine: Engine = ENGINE) -> None:
        self.engine: Engine = engine

    def fetch_all_review_id(self) -> list[str]:

        # SQL実行
        result_proxy = self.engine.execute(SELECT_ALL_REVIEW_ID_STATEMENT)

        return [review.review_id for review in result_proxy]

    def save_review_list(self, review_list: list[Review]) -> int:

        count = 0
        # トランザクション開始
        with self.engine.begin() as conn:
            for review in review_list:
                try:
                    count += conn.execute(INSERT_REVIEW_STATEMENT, {
                        "review_id": review.review_id,
                        "movie_id": review.movie_id,
                        "review": review.review_without_emoji
                    }).rowcount
                except IntegrityError:
                    pass
                except DataError:
                    log.exception("データ不正が発生しました.")

        return count
