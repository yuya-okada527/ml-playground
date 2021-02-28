"""Solrスキーマモデルモジュール

Solrのスキーマ変更APIのモデルを記述するモジュール
"""
from typing import Any

from pydantic import BaseModel, Field


class SolrResponseHeader(BaseModel):
    """Solrレスポンスヘッダー"""
    status: int
    QTime: int


class SolrSchemaModel(BaseModel):
    """Solrスキーマモデル"""
    name: str
    version: float
    uniqueKey: str
    fieldTypes: list[dict[str, Any]] = []
    fields_: list[dict[str, Any]] = Field([], alias="fields")
    dynamicFields: list[dict[str, Any]] = []
    copyFields: list[dict[str, Any]] = []


class SolrSchemaResponseModel(BaseModel):
    """Solrスキーマレスポンスモデル"""
    responseHeader: SolrResponseHeader
    schema_: SolrSchemaModel = Field(alias="schema")
