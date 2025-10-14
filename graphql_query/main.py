from typing import TypeVar, Union, Any
from dataclasses import is_dataclass, asdict

from pydantic import BaseModel

from graphql_query.types import (
    GraphQlQuery,
    GraphQlModel,
    GraphQlMethodType,
)
from graphql_query.converter.pydantic_ import get_graph_ql_models

Dataclass = TypeVar("Dataclass")


def build_inputs(data: Union[BaseModel, dict, Dataclass, None] = None) -> dict[str, Any] | None:
    conditions = (
        (isinstance(data, dict), lambda: data),
        (isinstance(data, BaseModel), lambda: data.model_dump(mode="python")),
        (is_dataclass(data), lambda: asdict(data))
    )
    return next((func for c, func in conditions if c), lambda: None)()


def build_models(schemas: list[type[BaseModel]]) -> list[GraphQlModel]:
    conditions = (
        (issubclass(schemas[0], BaseModel), get_graph_ql_models),
    )
    return next((func for c, func in conditions if c), lambda *_: None)(schemas)


def build_query(
    type_: GraphQlMethodType,
    name_method: str,
    *schemas: Union[BaseModel, dict, Dataclass],
    name: str = "Default",
    inputs: Union[BaseModel, dict, Dataclass, None] = None,
    query_mapping_types: dict[type, str] | None = None,
) -> GraphQlQuery:
    return GraphQlQuery(
        type_=type_,
        name=name,
        name_method=name_method,
        inputs=build_inputs(inputs),
        query_mapping_types=query_mapping_types,
        models=build_models(schemas),
    )
