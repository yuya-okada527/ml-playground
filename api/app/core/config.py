from pydantic import BaseSettings


class SolrSettings(BaseSettings):
    host: str
    port: int
    protocol: str
    collection: str

    def get_url(self) -> str:
        return f"{self.protocol}://{self.host}:{self.port}/solr"
    
    class Config:
        env_file = "env/solr.env"
