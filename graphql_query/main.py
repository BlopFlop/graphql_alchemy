from functools import wraps
from typing import TypeVar, Type, Awaitable

from pydantic import BaseModel

from graphql_query.converter import DataConverter
from graphql_query.types import GraphQlMethodType, GraphQlQuery

Dataclass = TypeVar('Dataclass')


def graphql_method(type: GraphQlMethodType, name: str,):
    def decorator(func: Awaitable):
        wraps(func)

        async def wrapper(
            *schemas: Type[BaseModel] | Type[Dataclass] | dict,
            name_query: str = "MyQuery",
            input_data: BaseModel | Dataclass | dict | None = None,
            query_mapping_types: dict[str, str] | None = None,
            **kwargs,
        ):
            converter = DataConverter(*schemas, input_data=input_data)
            query = GraphQlQuery(
                type_method=type,
                name=name_query,
                name_method=name,
                inputs=converter.input_types,
                query_mapping_types=query_mapping_types,
                models=converter.models,
            )
            vairables = converter.vairables(input_data)

            result_data = await func(query=str(query), vairables=vairables, **kwargs)

            return converter.output_data(result_data)
        return wrapper
    return decorator
