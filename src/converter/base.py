from typing import Any, Type, Union, Callable
from pydantic import BaseModel
from dataclasses import is_dataclass, asdict, fields

from ..types import GraphQlModel
from ..converter import dataclass_, pydantic_, dict_


class DataConverter:
    model_resolvers: dict[type, Callable] = {
        dict: dict_.build_graph_ql_models,
        BaseModel: pydantic_.build_graph_ql_models,
        dataclass_.Dataclass: dataclass_.build_graph_ql_models,
    }

    @staticmethod
    def _get_type(obj: Any) -> type:
        if is_dataclass(obj):
            return dataclass_.Dataclass
        elif isinstance(obj, type):
            return BaseModel if issubclass(obj, BaseModel) else obj 
        else:
            return BaseModel if issubclass((type_obj := type(obj)), BaseModel) else type_obj

    def _check_type_schemas(self) -> type:
        schema, *schemas = self.schemas
        type_ = self._get_type(schema)
        for schema in schemas:
            cur_type = self._get_type(schema)
            if type_ != cur_type:
                raise TypeError(f"All schemas must be of the same type. type: {type_} != type: {cur_type}")
        return type_

    def __init__(
        self,
        *schemas: list[Type[BaseModel] | Type[dataclass_.Dataclass] | dict],
        input_data: Union[BaseModel, dict, dataclass_.Dataclass, None] = None,
    ):
        self.input_data = input_data
        self.schemas = schemas

        self._schemas_type = self._check_type_schemas()
        self._input_type = self._get_type(self.input_data)

    @property
    def input_types(self) -> dict[str, Any] | None:
        resolve_pydantic = lambda: {field: getattr(self.input_data, field) for field in self.input_data.model_dump().keys()}  # noqa
        resolve_dataclass = lambda: {field.name: getattr(self.input_data, field.name) for field in fields(self.input_data)}  # noqa

        resolvers: dict[type, Callable] = {
            dict: lambda: self.input_data,
            BaseModel: resolve_pydantic,
            dataclass_.Dataclass: resolve_dataclass
        }
        return resolvers.get(self._input_type, lambda: None)()

    @property
    def vairables(self) -> dict[str, Any] | None:
        resolvers: dict[type, Callable] = {
            dict: lambda: self.input_data,
            BaseModel: lambda: self.input_data.model_dump(mode="json"),
            dataclass_.Dataclass: lambda: asdict(self.input_data),
        }
        return resolvers.get(self._input_type, lambda: None)()

    @property
    def models(self) -> list[GraphQlModel]:
        if resolver := self.model_resolvers.get(self._schemas_type):
            return resolver(self.schemas)

        raise TypeError(f"Schemas has bad type. type: {self._schemas_type} is bad")

    def __call__(self, output_data: dict[str, Any]) -> Union[BaseModel, dict, dataclass_.Dataclass]:
        resolvers = {
            dict: lambda: output_data,
            BaseModel: lambda: pydantic_.build_schema_from_data(output_data, *self.schemas),
            dataclass_.Dataclass: lambda: dataclass_.build_schema_from_data(output_data, *self.schemas),
        }

        if resolver := resolvers.get(self._schemas_type):
            return resolver()

        raise TypeError(f"Schemas has bad type. type: {self._schemas_type} is bad")
