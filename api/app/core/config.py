from pydantic import BaseSettings


class SolrSettings(BaseSettings):
    solr_host: str
    solr_port: int
    solr_protocol: str
    solr_collection: str

    def get_url(self) -> str:
        return f"{self.solr_protocol}://{self.solr_host}:{self.solr_port}/solr"
    
    class Config:
        env_file = "env/solr.env"