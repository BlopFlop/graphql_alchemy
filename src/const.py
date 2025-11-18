import uuid

from datetime import date, datetime
from typing import Final

from .types import GraphQlField, GraphQlModel, GraphQlTypeValue

QUERY_DEFAULT_NAME = "AutoGenQuery"

TYPENAME_FIELD: Final[GraphQlField] = GraphQlField(name="__typename", type=str)

RETURN_ERROR: Final[GraphQlModel] = GraphQlModel(
    name="ReturnError",
    fields=[
        TYPENAME_FIELD,
        GraphQlField(name="name", type=str),
        GraphQlField(name="message", type=str),
    ]
)

String: Final[GraphQlTypeValue] = GraphQlTypeValue(type=str, graph_type="String")
Int: Final[GraphQlTypeValue] = GraphQlTypeValue(type=int, graph_type="Int")
Float: Final[GraphQlTypeValue] = GraphQlTypeValue(type=float, graph_type="Float")
Boolean: Final[GraphQlTypeValue] = GraphQlTypeValue(type=bool, graph_type="Boolean")
Date: Final[GraphQlTypeValue] = GraphQlTypeValue(type=date, graph_type="Date")
DateTime: Final[GraphQlTypeValue] = GraphQlTypeValue(type=datetime, graph_type="DateTime")
UUID: Final[GraphQlTypeValue] = GraphQlTypeValue(type=uuid.UUID, graph_type="UUID")
