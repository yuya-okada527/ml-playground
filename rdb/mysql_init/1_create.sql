CREATE DATABASE input_db;
use input_db;

-- 映画テーブル
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
);

-- 映画ジャンルテーブル
CREATE TABLE IF NOT EXISTS `movie_genres` (
  `movie_id`        INT NOT NULL,
  `genre_id`        INT NOT NULL,
  PRIMARY KEY(`movie_id`, `genre_id`)
);

-- ジャンルテーブル
CREATE TABLE IF NOT EXISTS `genres` (
  `genre_id`      INT NOT NULL PRIMARY KEY,
  `name`          VARCHAR(64),
  `japanese_name` VARCHAR(64)
);

-- レビューテーブル
CREATE TABLE IF NOT EXISTS `reviews` (
  `review_id`   VARCHAR(64) NOT NULL PRIMARY KEY,
  `movie_id`    INT NOT NULL,
  `review`      TEXT
);

-- 類似映画テーブル
CREATE TABLE IF NOT EXISTS `similar_movies` (
  `movie_id`          INT NOT NULL,
  `similar_movie_id`  INT NOT NULL,
  PRIMARY KEY(`movie_id`, `similar_movie_id`)
);
