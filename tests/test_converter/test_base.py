from typing import Callable
from dataclasses import is_dataclass, asdict

import pytest
from pydantic import BaseModel

from src.converter import DataConverter, dataclass_, dict_, pydantic_

from tests.test_query import test_dataclass, test_dict, test_pydantic


@pytest.mark.parametrize(
    "inputs",
    (
        test_dataclass.third_input,
        test_pydantic.third_input,
        test_dict.third_input_data,
    )
)
def test_input_types(inputs):
    converter = DataConverter({'test_schema': None}, input_data=inputs)
    input_types = converter.input_types
    assert input_types == test_dict.third_input_data


@pytest.mark.parametrize(
    "inputs",
    (
        test_dataclass.third_input,
        test_pydantic.third_input,
        test_dict.third_input_data,
    )
)
def test_vairables(inputs):
    converter = DataConverter({'test_schema': None}, input_data=inputs)
    assert converter.input_types == test_dict.third_input_data


@pytest.mark.parametrize(
    "schemas, resolver",
    (
        ((test_dataclass.Research, test_dataclass.ReturnError), dataclass_.build_graph_ql_models),
        ((test_pydantic.Research, test_pydantic.ReturnError), pydantic_.build_graph_ql_models),
        ((test_dict.research_data, test_dict.return_error_data), dict_.build_graph_ql_models),
    )
)
def test_models(schemas, resolver: Callable):
    converter = DataConverter(*schemas)
    assert converter.models == resolver(schemas)


@pytest.mark.parametrize(
    "schemas, check_func",
    (
        ((test_dataclass.Research, test_dataclass.ReturnError), lambda x: is_dataclass(x)),
        ((test_pydantic.Research, test_pydantic.ReturnError), lambda x: isinstance(x, BaseModel)),
        ((test_dict.research_data, test_dict.return_error_data), lambda x: isinstance(x, dict)),
    )
)
def test_output_data(schemas, check_func):
    converter = DataConverter(*schemas)

    assert (result := converter(test_dict.research_data))
    assert check_func(result)


@pytest.mark.parametrize(
    "schemas",
    (
        (test_dataclass.Research, test_pydantic.ReturnError),
        (test_pydantic.Research, test_dataclass.ReturnError),
        (test_dict.research_data, test_pydantic.ReturnError),
    )
)
def test_type_schema_error(schemas):
    with pytest.raises(TypeError):
        DataConverter(*schemas)



@pytest.mark.parametrize(
    "schemas",
    (
        ([1,2,3], [1,2,3]),
        (123, 123),
        ("asf", "def"),
    )
)
def test_model_type_schema_error(schemas):
    with pytest.raises(TypeError):
        converter = DataConverter(*schemas)
        converter.models


@pytest.mark.parametrize(
    "schemas",
    (
        ([1,2,3], [1,2,3]),
        (123, 123),
        ("asf", "def"),
    )
)
def test_model_type_call_error(schemas):
    with pytest.raises(TypeError):
        converter = DataConverter(*schemas)
        converter({"test": "test1"})


@pytest.mark.parametrize(
    "variables, func",
    (
        (test_dataclass.third_input, lambda: asdict(test_dataclass.third_input)),
        (test_pydantic.third_input, lambda: test_pydantic.third_input.model_dump(mode="json")),
        (test_dict.third_input_data, lambda: test_dict.third_input_data),
        ([1,32,4], lambda: None),
        (None, lambda: None)
    )
)
def test_variables(variables, func):
    converter = DataConverter(
        test_pydantic.ReturnError,
        test_pydantic.ReturnError,
        input_data=variables
    )
    assert converter.vairables == func()
