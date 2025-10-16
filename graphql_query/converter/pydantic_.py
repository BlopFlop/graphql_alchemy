from typing import Any, Union, get_origin, get_args

from pydantic import BaseModel
from pydantic_core import PydanticUndefined
from pydantic.fields import FieldInfo

from graphql_query.types import GraphQlModel, GraphQlField


def get_pydantic_model_from_field_annotate(field_info: FieldInfo) -> BaseModel | None:
    annotation = field_info.annotation

    if issubclass(annotation, BaseModel):
        return annotation

    origin = get_origin(annotation)
    if origin is not None:
        args = get_args(annotation)

        # Optional[Model] -> Union[Model, None]
        if origin is Union:
            for arg in args:
                if issubclass(arg, BaseModel):
                    return arg

        # list[Model]
        for arg in args:
            if issubclass(arg, BaseModel):
                return arg

    return None


def get_defaul_field_value(schema: type[BaseModel], field_name: str) -> Any | None:
    field_info = schema.model_fields.get(field_name)

    if not field_info or field_info.default is PydanticUndefined:
        return None

    return field_info.default


def bind_graph_ql_model(
    schema: type[BaseModel],
    name_model: str | None = None,
    visited: set[type] = None
) -> GraphQlModel:
    visited = set() if visited is None else visited
    visited.add(schema)

    fiedls = []
    for name, info in schema.model_fields.items():
        inner_schema = get_pydantic_model_from_field_annotate(info)

        graph_ql_item = (
            bind_graph_ql_model(inner_schema, name, visited)
            if inner_schema and inner_schema not in visited
            else
            GraphQlField(name=info.alias or name)
        )
        fiedls.append(graph_ql_item)

    name_model = (
        get_defaul_field_value(schema, "typename") or schema.__name__
        if name_model is None
        else
        name_model
    )
    return GraphQlModel(name=name_model, fields=fiedls)


def get_graph_ql_models(schemas: list[type[BaseModel]]) -> list[GraphQlModel]:
    return [bind_graph_ql_model(schema) for schema in schemas]