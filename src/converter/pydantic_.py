import logging
from typing import Any, Union, get_origin, get_args, Type

from pydantic import BaseModel, ValidationError
from pydantic_core import PydanticUndefined
from pydantic.fields import FieldInfo

from ..types import GraphQlModel, GraphQlField


TYPENAME_FIELD = "typename"


def get_pydantic_model_from_field_annotate(field_info: FieldInfo) -> BaseModel | None:
    annotation = field_info.annotation

    if isinstance(annotation, type) and issubclass(annotation, BaseModel):
        return annotation

    origin = get_origin(annotation)
    if origin is not None:
        args = get_args(annotation)

        # Optional[Model] -> Union[Model, None]
        if origin is Union:
            for arg in args:
                if isinstance(annotation, type) and issubclass(annotation, BaseModel):
                    return arg

        # list[Model]
        for arg in args:
            if isinstance(arg, type) and issubclass(arg, BaseModel):
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


def build_graph_ql_models(schemas: list[type[BaseModel]]) -> list[GraphQlModel]:
    return [bind_graph_ql_model(schema) for schema in schemas]


def handler_validation(data: dict[str, Any], type_schema: Type[BaseModel]) -> BaseModel | None:
    try:
        return type_schema(**data)
    except ValidationError as e:
        logging.debug(f'Data for schema {type_schema.__name__} is not valid: {e}')
    return None


def build_schema_from_data(data: dict[str, Any], *type_schemas: Type[BaseModel]) -> BaseModel:
    if not type_schemas:
        raise ValueError("Type schemas is empty")

    schema = next((
        res for t_s in type_schemas
        if (res := handler_validation(data, t_s))
    ), None)

    if schema is None:
        schema_names = [t_s.__name__ for t_s in type_schemas]
        raise TypeError(f"Niether of the schemas {schema_names} valid for data. Data: {data}")

    return schema
