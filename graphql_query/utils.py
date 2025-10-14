from enum import StrEnum
from typing import Any, Type

from .types.base import GraphQlModel, GraphQlField


def inputs_to_graphql_mapping(
    data: dict[str, Any],
    type_to_graphql_mapping: dict[Type[Any], StrEnum] = None,
) -> str:
    get_name_map_type_or_type = lambda v: type_to_graphql_mapping.get(type(v)) or v.__class__.__name__  # noqa

    result = []
    for field, values in data.items():
        if isinstance(values, list):
            if not values:
                continue

            value = values[0]
            map_type = get_name_map_type_or_type(value)
            result.append(f"${field}: [{map_type}!]")
            continue

        map_type = get_name_map_type_or_type(values)

        result.append(f"${field}: {map_type}")
    return ", ".join(result)


def inputs_to_graphql(data: dict[str, Any]) -> str:
    return ", ".join(f"{field}: ${field}" for field in data.keys())


def models_to_graphql(models: list[GraphQlModel, GraphQlField]) -> str:
    result = " ".join(f"... on {str(model)}" for model in models)
    return f"{{{result}}}"
