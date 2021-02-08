from pydantic import BaseModel, Field


class SolrResponseHeader(BaseModel):
    status: int
    QTime: int


class SolrSchemaModel(BaseModel):
    name: str
    version: float
    uniqueKey: str
    fieldTypes: list[dict]
    fields_: list[dict] = Field(alias="fields")
    dynamicFields: list[dict]
    copyFields: list[dict]


class SolrSchemaResponseModel(BaseModel):
    responseHeader: SolrResponseHeader
    schema_: SolrSchemaModel = Field(alias="schema")
