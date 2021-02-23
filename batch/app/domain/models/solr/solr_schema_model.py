from typing import Any

from pydantic import BaseModel, Field


class SolrResponseHeader(BaseModel):
    status: int
    QTime: int


class SolrSchemaModel(BaseModel):
    name: str
    version: float
    uniqueKey: str
    fieldTypes: list[dict[str, Any]]
    fields_: list[dict[str, Any]] = Field(alias="fields")
    dynamicFields: list[dict[str, Any]]
    copyFields: list[dict[str, Any]]


class SolrSchemaResponseModel(BaseModel):
    responseHeader: SolrResponseHeader
    schema_: SolrSchemaModel = Field(alias="schema")
