from enum import Enum, StrEnum
from datetime import date
from typing import Type, Generic, TypeVar, Callable

from pydantic import BaseModel, Field, model_validator

from .enums import TypeMethod

T = TypeVar("T")


def _enum_to_str(v: Enum) -> str:
    return f"{v.value}"


input_type_convert_to_string_hadlers: dict[type, Callable] = {
    date: lambda v: f"'{str(v)}'",
    str: lambda v: f"'{v}'",
    bool: lambda v: "true" if v else "false",
    Enum: _enum_to_str,
    StrEnum: _enum_to_str
}


class GraphQlField(BaseModel):
    name: str
    type: Type

    def __str__(self) -> str:
        return self.name


class InputGraphQlField(GraphQlField, Generic[T]):
    value: T

    @model_validator(mode="after")
    def value_validate(self):
        if not isinstance(self.value, self.type):
            raise TypeError(f"Incorrect value type {type(self.value)} != {self.type}")
        return self

    def __str__(self) -> str:
        value = (
            handler(self.value)
            if (handler := input_type_convert_to_string_hadlers.get(self.type))
            else
            str(self.value)
        )
        return f"{self.name}: {value}"


class GraphQlModel(BaseModel):
    name: str
    fields: list["GraphQlField | GraphQlModel"] = Field(min_length=1)

    def __str__(self):
        model_fields = " ".join(str(field) for field in self.fields)
        return f"{self.name} {{{model_fields}}}"


class InputGraphQlModel(BaseModel):
    name: str
    inputs: list["InputGraphQlField | InputGraphQlModel"] = Field(min_length=1)

    def __str__(self) -> str:
        input_fields = ", ".join(str(input_) for input_ in self.inputs)
        return f"{self.name}: {{{input_fields}}}"


class GraphQlMethod(BaseModel):
    type: TypeMethod
    name: str
