from typing import Any, Type

from pydantic import BaseModel, Field, model_validator

from .base import GraphQlModel
from .enums import GraphQlMethodType
from ..const import String, Int, Float, Boolean, Date, DateTime, UUID
from ..utils import inputs_to_graphql_mapping, models_to_graphql


class GraphQlQuery(BaseModel):
    """
    Query builder schema
    - Example:

    Map parameters.
    ```
    {type} {name}({inputs"fst_ground_keys": query_mapping_types.value}) {
        {name_method}({inputs"fst_ground_keys"}) {
            ... on {GraphQlModel.name} {GraphQlModel.name, GraphQlField.name}
        }
    }
    ```

    Result query.
    ```
    mutation Default($fst_ground_key: FstGroundKey!) {
        UpdateElements(fst_ground_key: $fst_ground_key) {
            ... on ReturnError {
                __typename
                message
                name
            }
            ... on TestModel {
                field_uuid
                test_model_inner {
                    inner_field_1
                    inner_field_2
                    inner_field_3 {
                        inner_inner_field_4
                    }
                }
            }
        }
    }
    ```
    """
    type_method: GraphQlMethodType
    name: str = "Default"
    name_method: str
    inputs: dict[str, Any] | None = None
    query_mapping_types: dict[Type, str] | None = Field(default_factory=lambda: {})
    models: list[GraphQlModel]

    @model_validator(mode="after")
    def bind_mapping_types(self) -> None:
        self.query_mapping_types = (
            self.query_mapping_types
            if self.query_mapping_types
            else
            {}
        )
        for type_ in (String, Int, Float, Boolean, Date, DateTime, UUID):
            self.query_mapping_types[type_.type] = type_.graph_type
        return self

    def __str__(self) -> str:
        fields = models_to_graphql(self.models)

        if self.inputs:
            fields_to_type, fields_to_fileds = inputs_to_graphql_mapping(self.inputs, self.query_mapping_types)
            mapping, inputs = f"({fields_to_type})", f"({fields_to_fileds})"
        else:
            mapping, inputs = "", ""

        return f"{self.type_method} {self.name}{mapping} {{{self.name_method}{inputs} {fields}}}"
