from pydantic import BaseModel


class Tag(BaseModel):
    name: str
    color: str


class Post(BaseModel):
    title: str
    content: Tag
    tags: dict[str, Tag]
    is_published: list[Tag] = False


from pydantic import BaseModel
from pydantic.fields import FieldInfo
from typing import get_origin, get_args, Union, Optional, List, Dict


def get_pydantic_model_from_field(field_info: FieldInfo):
    """Извлекает Pydantic модель из поля, если она есть"""
    annotation = field_info.annotation

    if issubclass(annotation, BaseModel):
        return annotation

    origin = get_origin(annotation)
    if origin is not None:
        args = get_args(annotation)

        # Optional[Model] -> Union[Model, None]
        if origin is Union:
            for arg in args:
                if isinstance(arg, type) and issubclass(arg, BaseModel):
                    return arg

        # list[Model]
        for arg in args:
            if issubclass(arg, BaseModel):
                return arg

    return None


def get_fields_from_pydantic(schema: type[BaseModel]) -> dict[str, None | dict]:
    result = {
        name: (
            get_fields_from_pydantic(inner_schema)
            if (inner_schema := get_pydantic_model_from_field(info))
            else
            None
        )
        for name, info in schema.model_fields.items()
    }
    return result

print(get_fields_from_pydantic(Post))
