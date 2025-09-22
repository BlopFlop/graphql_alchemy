from typing import Any

from pydantic import BaseModel

from graphql_alchemy.adapters import AbstractAdapter
from graphql_alchemy.query import query
from graphql_alchemy.const import RETURN_ERROR
from graphql_alchemy.types import GraphQlField, GraphQlModel, InputGraphQlField, InputGraphQlModel, GraphQlMethod


def _graph_ql_inputs_from_schema(
    schema: BaseModel,
) -> list[GraphQlModel | GraphQlField]:
    result = []

    for field in schema.model_fields_set:
        value = getattr(schema, field)

        if isinstance(value, BaseModel):
            inputs = _graph_ql_inputs_from_schema(value)
            graphql_input = InputGraphQlModel(name=field, inputs=inputs)
            result.extend(graphql_input)

        else:
            result.append(InputGraphQlField(name=field, type=type(value), value=value))

    return result 


def _graph_ql_from_type_schema(type_schemas: list[type[BaseModel]]) -> list[GraphQlModel | GraphQlField]:
    pass


class PydanticAdapter(AbstractAdapter):

    def __init__(self, method: GraphQlMethod, result_schemas: list[type[BaseModel]], error_schema: BaseModel):
        self.method = method
        self.type_schemas = result_schemas

    def to_query(self, input_data: BaseModel | None = None):
        inputs = _graph_ql_inputs_from_schema(input_data)
        models = _graph_ql_from_type_schema(self.type_schemas)

        return query(type=self.method.type, name=self.method.name, inputs=inputs, models=models)

    def from_query(self, response_data: dict[str, Any]) -> BaseModel:
        data = response_data.get("data")

        if not data:
            raise ValueError

        method_data = response_data.get(self.method.name)

        if not method_data:
            raise ValueError
