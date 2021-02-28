import os
import shutil
import sqlite3

import pytest
from sqlalchemy.engine import create_engine
from sqlalchemy.engine.base import Connection, Engine, Transaction

# ---------------------------
# SQL
# ---------------------------
CREATE_MOVIES_TABLE = """\
CREATE TABLE IF NOT EXISTS `movies` (
  `movie_id`        INT NOT NULL PRIMARY KEY,
  `imdb_id`         VARCHAR(64),
  `original_title`  VARCHAR(256),
  `japanese_title`  VARCHAR(256),
  `overview`        TEXT,
  `tagline`         TEXT,
  `poster_path`     VARCHAR(256),
  `backdrop_path`   VARCHAR(256),
  `popularity`      FLOAT,
  `vote_average`    FLOAT,
  `vote_count`      INT,
  `release_date`    CHAR(10)
)
"""
CREATE_MOVIE_GENRES_TABLE = """\
CREATE TABLE IF NOT EXISTS `movie_genres` (
  `movie_id`        INT NOT NULL,
  `genre_id`        INT NOT NULL,
  PRIMARY KEY(`movie_id`, `genre_id`)
)
"""
CREATE_GENRE_TABLE = """\
CREATE TABLE IF NOT EXISTS `genres` (
  `genre_id`      INT NOT NULL PRIMARY KEY,
  `name`          VARCHAR(64),
  `japanese_name` VARCHAR(64)
)
"""
CREATE_REVIEWS_TABLE = """\
CREATE TABLE IF NOT EXISTS `reviews` (
  `review_id`   VARCHAR(64) NOT NULL PRIMARY KEY,
  `movie_id`    INT NOT NULL,
  `review`      TEXT
)
"""
CREATE_SIMILAR_MOVIES_TABLE = """\
CREATE TABLE IF NOT EXISTS `similar_movies` (
  `movie_id`          INT NOT NULL,
  `similar_movie_id`  INT NOT NULL,
  PRIMARY KEY(`movie_id`, `similar_movie_id`)
)
"""
INIT_DATABASE_SQL_LIST= [
    # テーブル削除
    "DROP TABLE IF EXISTS `movies`",
    "DROP TABLE IF EXISTS `movie_genres`",
    "DROP TABLE IF EXISTS `genres`",
    "DROP TABLE IF EXISTS `genres`",
    "DROP TABLE IF EXISTS `reviews`",
    "DROP TABLE IF EXISTS `similar_movies`",
    # テーブル作成
    CREATE_MOVIES_TABLE,
    CREATE_MOVIE_GENRES_TABLE,
    CREATE_GENRE_TABLE,
    CREATE_REVIEWS_TABLE,
    CREATE_SIMILAR_MOVIES_TABLE
]


@pytest.fixture(scope="session")
def test_engine():

    # sqliteのDBを作成
    db_dir = "src/tests/data/temp"
    os.makedirs(db_dir, exist_ok=True)
    db_name = f"{db_dir}/database.db"
    conn = sqlite3.connect(db_name)
    conn.close()

    # テスト用のエンジンを作成
    engine = create_engine(f"sqlite:///{db_name}")

    # テーブルを初期化
    for init_sql in INIT_DATABASE_SQL_LIST:
        engine.execute(init_sql)

    yield engine

    # テンプディレクトリを削除
    shutil.rmtree(db_dir)


@pytest.fixture
def conn(test_engine: Engine):

    conn: Connection = test_engine.connect()

    transaction: Transaction = conn.begin()

    yield conn

    transaction.rollback()
    conn.close()
