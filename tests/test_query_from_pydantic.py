from typing import Literal
from uuid import UUID

from graphql_query.types import GraphQlMethodType

# from graphql_query.converter.pydantic_ import
import pytest
from pydantic import BaseModel, Field

from graphql_query.main import build_query


class ReturnError(BaseModel):
    typename: Literal["ReturnError"] = Field(default="ReturnError", alias="__typename")
    message: str
    name: str


class Fst(BaseModel):
    typename: str = Field(default="TestModel", alias="__typename")
    simple: str


fst_query = """query MyQuery {test_query {... on TestModel {__typename simple} ... on ReturnError {__typename message name}}}"""


class Snd(BaseModel):
    simple: str
    integer: int
    uuid_: UUID
    float_: float
    boolean: bool
    list_: list


snd_query = """query MyQuery {test_query {... on Snd {simple integer uuid_ float_ boolean list_}}}"""


@pytest.mark.parametrize(
    "schemas, check_query",
    (
        ((Fst, ReturnError), fst_query),
        ((Snd, ), snd_query),
    )
)
def test_build_query(schemas, check_query):
    query = build_query(
        GraphQlMethodType.query,
        "test_query",
        *schemas,
        name="MyQuery"
    )
    assert str(query) == check_query
