from typing import Final

from .types import GraphQlField, GraphQlModel

TYPENAME_FIELD: Final[GraphQlField] = GraphQlField(name="__typename", type=str)

RETURN_ERROR: Final[GraphQlModel] = GraphQlModel(
    name="ReturnError",
    fields=[
        TYPENAME_FIELD,
        GraphQlField(name="name", type=str),
        GraphQlField(name="message", type=str),
    ]
)
