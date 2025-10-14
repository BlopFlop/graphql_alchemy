from typing import Any, Union, get_origin, get_args

from pydantic import BaseModel
from pydantic_core import PydanticUndefined
from pydantic.fields import FieldInfo

from graphql_query.types import GraphQlModel, GraphQlField


def get_pydantic_model_from_field_annotate(field_info: FieldInfo, visited: set[type[BaseModel]] = None) -> BaseModel | None:
    if visited is None:
        visited = set()

    annotation = field_info.annotation

    if annotation in visited:
        return None

    visited.add(annotation)

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


def get_fields_from_pydantic(schema: type[BaseModel]) -> dict[str, None | dict]:
    result = {
        name: (
            get_fields_from_pydantic(inner_schema)
            if (inner_schema := get_pydantic_model_from_field_annotate(info))
            else
            None
        )
        for name, info in schema.model_fields.items()
    }
    return result


def get_defaul_field_value(schema: type[BaseModel], field_name: str):
    field_info = schema.model_fields.get(field_name)

    if not field_info or field_info.default is PydanticUndefined:
        return None

    return field_info.default


def bind_graph_ql_model(schema: type[BaseModel]) -> GraphQlModel:
    name_model = get_defaul_field_value(schema, "typename") or schema.__name__
    return GraphQlModel(name=name_model, fields=[
        (
            bind_graph_ql_model(inner_schema)
            if (inner_schema := get_pydantic_model_from_field_annotate(info))
            else
            GraphQlField(name=info.alias or name)
        )
        for name, info in schema.model_fields.items()
    ])


def get_graph_ql_models(schemas: list[type[BaseModel]]) -> list[GraphQlModel]:
    return [bind_graph_ql_model(schema) for schema in schemas]