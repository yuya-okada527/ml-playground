"""設定モジュール

設定クラスを記述するモジュール
ローカル開発環境起動時は、プロジェクトルート配下のenvディレクトリ内のenvファイルを利用
本番環境では、環境変数の値を利用する
"""
from typing import Any

from domain.enums.core_enums import LogLevel
from pydantic import BaseSettings


class CoreSettings(BaseSettings):
    """コア設定クラス

    バッチアプリ全体に関係する設定を保持する

    Attributes:
        batch_log_level: ログレベル
    """
    batch_log_level: LogLevel

    class Config:
        env_file = "env/core.env"


class TmdbSettings(BaseSettings):
    """TMDB設定クラス

    TMDBに対する設定情報を保持する

    Attributes:
        tmdb_api_key: APIキー
        tmdb_url: TMDBのURL
    """
    tmdb_api_key: str
    tmdb_url: str = "https://api.themoviedb.org/3"

    class Config:
        env_file = "env/tmdb.env"


class InputDbSettings(BaseSettings):
    """インプットDB設定クラス

    インプットDBに対する設定情報を保持する

    Attributes:
        input_db_engine: DBエンジン
        input_db_host: ホスト
        input_db_port: ポート
        input_db_user: ユーザ
        input_db_password: パスワード
        input_db_database: データベース
    """
    input_db_engine: str = "mysql+pymysql"
    input_db_host: str = "localhost"
    input_db_port: int = 3306
    input_db_user: str = "user"
    input_db_password: str = "password"
    input_db_database: str = "input_db"

    def get_connection_config(self) -> dict[str, Any]:
        """DB接続情報取得関数

        DBに対する接続情報を取得する
        """
        return {
            "default": {
                "engine": self.input_db_engine,
                "credentials": {
                    "host": self.input_db_host,
                    "port": self.input_db_port,
                    "user": self.input_db_user,
                    "password": self.input_db_password,
                    "database": self.input_db_database
                }
            }
        }

    class Config:
        env_file = "env/input_db.env"


class SolrSettings(BaseSettings):
    """Solr設定クラス

    Solrに関する設定情報クラス

    Attributes:
        solr_protocol: プロトコル
        solr_host: ホスト
        solr_port: ポート
        solr_collection: コレクション
    """
    solr_protocol: str = "http"
    solr_host: str
    solr_port: int
    solr_collection: str

    def get_url(self) -> str:
        """接続URL取得関数

        接続URLを取得する
        """
        return f"{self.solr_protocol}://{self.solr_host}:{self.solr_port}"

    class Config:
        env_file = "env/solr.env"


class RedisSettings(BaseSettings):
    """Redis設定クラス

    Redisに関する設定情報クラス

    Attributes:
        redis_protocol: プロトコル
        redis_host: ホスト
        redis_port: ポート
    """
    redis_protocol: str = "http"
    redis_host: str = "localhost"
    redis_port: int = 6379

    class Config:
        env_file = "env/redis.env"
