from typing import Any

import pytest
from pydantic import BaseModel
from src.converter.pydantic_ import handler_validation, build_schema_from_data


class UserSchema(BaseModel):
    id: int
    name: str
    email: str


class ProductSchema(BaseModel):
    product_id: int
    title: str
    price: float


class OrderSchema(BaseModel):
    order_id: int
    user_id: int
    total: float


class OptionalSchema(BaseModel):
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
    schema: type[BaseModel],
):
    result = handler_validation(data, schema)

    assert isinstance(result, schema)
    dict_data = result.model_dump(mode='json')
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
def test_build_schema(data: dict[str, Any], schemas: list[BaseModel], good_schema: type[BaseModel]):
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
