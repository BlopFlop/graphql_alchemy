import logging
from dataclasses import is_dataclass, asdict, fields
from typing import Any, Union, TypeVar, overload, Type
from python_graphql_client import GraphqlClient

from pydantic import BaseModel

from graphql_query.converter import pydantic_converter, dataclass_converter, dict_converter
from .enums import GraphQlMethodType
from .headers import Headers
from .query import GraphQlQuery, GraphQlModel

Dataclass = TypeVar('Dataclass')


class GraphQlMethod(BaseModel):
    type: GraphQlMethodType
    name: str
    client: GraphqlClient

    @staticmethod
    def _build_variables_from_input_data(input: Union[BaseModel, dict, Dataclass, None] = None) -> dict[str, Any] | None:
        conditions = (
            (isinstance(input, dict), lambda: input),
            (isinstance(input, BaseModel), lambda: input.model_dump(mode="json")),
            (is_dataclass(input), lambda: asdict(input))
        )
        return next((func for c, func in conditions if c), lambda *_: None)

    @staticmethod
    def _build_query_inputs_from_input(input: Union[BaseModel, dict, Dataclass, None] = None) -> dict[str, Any] | None:
        func_pydantic = lambda: {field: getattr(input, field) for field in input.model_dump().keys()}  # noqa
        func_dataclass = lambda: {field: getattr(input, field) for field in fields(input)}

        conditions = (
            (isinstance(input, dict), lambda: input),
            (isinstance(input, BaseModel), func_pydantic),
            (is_dataclass(input), lambda: func_dataclass)
        )
        return next((func for c, func in conditions if c), lambda: None)()

    @staticmethod
    def _build_models_for_query(schemas: list[Type[BaseModel] | Type[Dataclass] | dict]) -> list[GraphQlModel]:
        conditions = (
            (isinstance(schemas[0], dict), dict_converter.build_graph_ql_models),
            (issubclass(schemas[0], BaseModel), pydantic_converter.build_graph_ql_models),
            (is_dataclass(schemas[0]), dataclass_converter.build_graph_ql_models),
        )
        return next((func for c, func in conditions if c), lambda *_: None)(schemas)

    @overload
    def _build_result_data(self, data: dict[str, Any], *schemas: Type[BaseModel]) -> BaseModel:
        ...

    @overload
    def _build_result_data(self, data: dict[str, Any], *schemas: Dataclass) -> Dataclass:
        ...

    def _build_result_data(
        self,
        data: dict[str, Any],
        *type_schemas: Type[BaseModel] | Type[Dataclass]
    ) -> Type[BaseModel] | Type[Dataclass]:
        if isinstance(type_schemas[0], BaseModel):
            return pydantic_converter.build_schema_from_data(data, type_schemas)
        return dataclass_converter.build_schema_from_data(data, type_schemas)

    @overload
    async def __call__(
        self,
        *schemas: Type[Dataclass],
        headers: Headers | None = None,
        input_: BaseModel | dict,
    ) -> list[Dataclass]:
        ...

    @overload
    async def __call__(
        self,
        *schemas: Type[BaseModel],
        headers: Headers | None = None,
        input_: BaseModel | dict,
    ) -> list[BaseModel]:
        ...

    @overload
    async def __call__(
        self,
        *schemas: dict,
        headers: Headers | None = None,
        input_: BaseModel | dict,
    ) -> list[dict]:
        ...

    async def __call__(
        self,
        *schemas: Type[BaseModel] | Type[Dataclass] | dict,
        name_query: str = "MyQuery",
        headers: Headers | None = None,
        input_data: BaseModel | Dataclass | dict | None = None,
        query_mapping_types: dict[str, str] | None = None,
    ) -> BaseModel | Type[Dataclass] | list[dict]:
        # Реализация метода
        headers = headers.model_dump() if headers else None
        query = GraphQlQuery(
            type_method=self.type,
            name=name_query,
            name_method=self.name,
            inputs=self._build_query_inputs_from_input(input_data),
            query_mapping_types=query_mapping_types,
            models=self._build_models_for_query(*schemas),
        )

        variables = self._build_variables_from_input_data(input_data)

        logging.debug((
            f"Send request in endpoint url {self.client.endpoint}\n"
            f"Query >> {str(query)}\n"
            f"variables >> {variables}\n"
        ))
        data = await self.client.execute_async(query=str(query), variables=variables, headers=headers,)
        logging.debug(f"Result_data {data}")

        return (
            data
            if isinstance(data, dict)
            else
            self._build_result_data(data, *schemas)
        )
