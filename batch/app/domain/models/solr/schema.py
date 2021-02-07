from pydantic import BaseModel


class SolrResponseHeader(BaseModel):
    status: int
    QTime: int


class SolrSchemaModel(BaseModel):
    name: str
    version: float
    uniqueKey: str
    fieldTypes: list[dict]
    fields: list[dict]
    dynamicFields: list[dict]
    copyFields: list[dict]


class SolrSchemaResponseModel(BaseModel):
    responseHeader: SolrResponseHeader
    schema: SolrSchemaModel
