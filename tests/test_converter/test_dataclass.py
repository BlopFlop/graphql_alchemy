from typing import Any
from pydantic.dataclasses import dataclass
import pytest
from src.converter.dataclass_ import handler_validation, build_schema_from_data


@dataclass
class UserSchema:
    id: int
    name: str
    email: str


@dataclass
class ProductSchema:
    product_id: int
    title: str
    price: float


@dataclass
class OrderSchema:
    order_id: int
    user_id: int
    total: float


@dataclass
class OptionalSchema:
    required_field: str
    optional_field: str = "default"


user_data = {"id": 1, "name": "John", "email": "john@test.com"}
product_data = {"product_id": 123, "title": "Test Product", "price": 99.99}
order_data = {"order_id": 456, "user_id": 1, "total": 150.0}


@pytest.mark.parametrize(
    "data, schema",
    (
        (user_data, UserSchema),
        (product_data, ProductSchema),
        (order_data, OrderSchema),
    )
)
def test_handler_validation_success(
    data: dict[str, Any],
    schema: type,
):
    result = handler_validation(data, schema)

    assert isinstance(result, schema)
    # Для датаклассов используем __dict__ вместо model_dump
    dict_data = result.__dict__
    assert data == dict_data


@pytest.mark.parametrize(
    "data",
    (
        {"id": 1, "name": "John"},
        {"id": "not_an_int", "name": "John", "email": "john@test.com"},
        {},
    )
)
def test_handler_validation_failure(data: dict[str, Any]):
    result = handler_validation(data, UserSchema)
    assert result is None


def test_handler_validation_extra_fields():
    data = {"id": 1, "name": "John", "email": "john@test.com", "extra_field": "value"}
    result = handler_validation(data, UserSchema)
    assert result is not None
    assert isinstance(result, UserSchema)


def test_build_schema_no_valid_schemas():
    data = {"invalid_field": "value"}
    with pytest.raises(TypeError):
        build_schema_from_data(data, UserSchema, ProductSchema, OrderSchema)


def test_build_schema_empty_schemas():
    data = {"id": 1, "name": "John", "email": "john@test.com"}
    with pytest.raises(ValueError):
        build_schema_from_data(data)


doube_schemas_data = {"id": 1, "name": "John", "email": "john@test.com", "product_id": 123, "title": "Product", "price": 99.99}


@pytest.mark.parametrize(
    "data, schemas, good_schema",
    (
        (user_data, (UserSchema,), UserSchema),
        (user_data, (ProductSchema, OrderSchema, UserSchema), UserSchema),
        (product_data, (ProductSchema, OrderSchema, UserSchema), ProductSchema),
        (order_data, (ProductSchema, OrderSchema, UserSchema), OrderSchema),
        (doube_schemas_data, (UserSchema, ProductSchema), UserSchema),
        (doube_schemas_data, (ProductSchema, UserSchema), ProductSchema),
    )
)
def test_build_schema(data: dict[str, Any], schemas: list, good_schema: type):
    result = build_schema_from_data(data, *schemas)
    assert isinstance(result, good_schema)


def test_build_schema_partial_match():
    partial_user_data = {"id": 1, "name": "John"}
    with pytest.raises(TypeError):
        build_schema_from_data(partial_user_data, UserSchema, ProductSchema)


def test_build_schema_single_schema_invalid():
    data = {"wrong_field": "value"}
    with pytest.raises(TypeError):
        build_schema_from_data(data, UserSchema)