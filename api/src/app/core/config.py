"""設定モジュール

設定クラスを記述するモジュール
ローカル開発環境起動時は、プロジェクトルート配下のenvディレクトリ内のenvファイルを利用
本番環境では、環境変数の値を利用する
"""
from pydantic import BaseSettings


class CoreSettings(BaseSettings):
    # カンマ区切りで設定可能FEドメイン
    fe_domain: str = "http://localhost:3000"


class SolrSettings(BaseSettings):
    solr_host: str
    solr_port: int
    solr_protocol: str
    solr_collection: str

    def get_url(self) -> str:
        return f"{self.solr_protocol}://{self.solr_host}:{self.solr_port}/solr"

    class Config:
        env_file = "env/solr.env"


class RedisSettings(BaseSettings):
    redis_protocol: str
    redis_host: str
    redis_port: int

    class Config:
        env_file = "env/redis.env"
