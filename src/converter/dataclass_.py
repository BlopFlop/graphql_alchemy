import logging
from typing import Any, Union, get_origin, get_args, TypeVar
from dataclasses import fields, is_dataclass, MISSING

from ..types import GraphQlModel, GraphQlField


Dataclass = TypeVar('Dataclass')

TYPENAME_FIELD = "typename"


def get_input_types(input_data: Dataclass):
    return {field: getattr(input_data, field) for field in fields(input_data)}  # noqa


def get_dataclass_from_field_annotate(annotation: Any) -> Any | None:
    if is_dataclass(annotation):
        return annotation

    origin = get_origin(annotation)
    if origin is not None:
        args = get_args(annotation)

        # Optional[DataClass] -> Union[DataClass, None]
        if origin is Union:
            for arg in args:

                result = get_dataclass_from_field_annotate(arg)
                if result is not None:
                    return result

        for arg in args:
            if is_dataclass(arg):
                return arg

            result = get_dataclass_from_field_annotate(arg)
            if result is not None:
                return result

    return None


def get_default_dataclass_value(
    dataclass_type: type[Dataclass],
    field_name: str
) -> Any | None:
    for field in fields(dataclass_type):
        if field.name != field_name:
            continue

        return (
            field.default
            if field.default is not MISSING
            else
            None
        )

    return None


def bind_graph_ql_model(
    schema: type[Dataclass],
    name_model: str | None = None,
    visited: set[type[Dataclass]] = None
) -> GraphQlModel:
    visited = set() if visited is None else visited
    visited.add(schema)

    graphql_fields = []

    for field in fields(schema):
        inner_dataclass = get_dataclass_from_field_annotate(field.type)

        graphql_item = (
            bind_graph_ql_model(inner_dataclass, field.name, visited)
            if inner_dataclass and inner_dataclass not in visited
            else
            GraphQlField(name=field.name)
        )

        if graphql_item.name == TYPENAME_FIELD:
            graphql_item.name = "__typename"

        graphql_fields.append(graphql_item)

    name_model = (
        get_default_dataclass_value(schema, TYPENAME_FIELD) or schema.__name__
        if name_model is None
        else
        name_model
    )

    return GraphQlModel(name=name_model, fields=graphql_fields)


def build_graph_ql_models(schemas: list[type[Dataclass]]) -> list[GraphQlModel]:
    return [bind_graph_ql_model(schema) for schema in schemas]


def handler_validation(data: dict[str, Any], type_schema: list[type[Dataclass]]) -> type[Dataclass] | None:
    try:
        class_fields = {field.name for field in fields(type_schema)}
        filtered_data = {key: data[key] for key in data.keys() & class_fields}
        return type_schema(**filtered_data)
    except (TypeError, ValueError) as e:
        logging.debug(f'Data for dataclass {type_schema.__name__} is not valid: {e}')
    return None


def build_schema_from_data(data: dict[str, Any], *type_schemas: type[Dataclass]) -> type[Dataclass]:
    if not type_schemas:
        raise ValueError("Type schemas is empty")

    schema = next((
        res for t_s in type_schemas
        if (res := handler_validation(data, t_s))
    ), None)

    if schema is None:
        schema_names = [t_s.__name__ for t_s in type_schemas]
        raise TypeError(f"Neither of the dataclasses {schema_names} valid for data. Data: {data}")

    return schema
