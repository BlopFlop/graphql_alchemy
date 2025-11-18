from typing import Any

from ..types import GraphQlModel, GraphQlField


TYPENAME_FIELD = "__typename"


def bind_graph_ql_model(
    data_dict: dict[str, Any],
    name_model: str,
    visited: set[str] = None
) -> GraphQlModel:
    visited = set() if visited is None else visited
    model_name = f"{name_model}Model"

    if model_name in visited:
        return GraphQlField(name=name_model)

    visited.add(model_name)

    fields = []

    for key, value in data_dict.items():
        if not value:
            fields.append(GraphQlField(name=key))

        elif isinstance(value, dict):
            nested_model = bind_graph_ql_model(value, key, visited.copy())
            fields.append(nested_model)

        elif isinstance(value, list) and value and isinstance(value[0], dict):
            nested_model = bind_graph_ql_model(value[0], key, visited.copy())
            fields.append(nested_model)
        else:
            fields.append(GraphQlField(name=key))

    return GraphQlModel(name=name_model, fields=fields)


def build_graph_ql_models(data_dicts: list[dict[str, Any]]) -> list[GraphQlModel]:
    """Строит GraphQL модели из списка словарей"""
    return [bind_graph_ql_model(data, data.get(TYPENAME_FIELD, "Not __typename field for name model")) for data in data_dicts]
