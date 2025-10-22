from collections.abc import Callable

from pydantic import AliasGenerator, BaseModel, ConfigDict, Field, field_validator


class Headers(BaseModel):
    authorization: str | None = Field(..., alias="Authorization")
    content_type: str | None = Field("application/json", alias="Content-Type")

    @classmethod
    def alias_reverse_generator(cls, alias: str) -> Callable[[str], str] | AliasGenerator | None:
        """Конвертирует 'Content-Type' -> 'content_type'"""
        return alias.lower().replace("-", "_")

    @field_validator("authorization", check_fields=False)
    @classmethod
    def bearer(cls, value: str) -> str:
        bearer = "Bearer "
        return (
            value
            if value.startswith(bearer)
            else
            bearer + value
        )

    model_config = ConfigDict(
        alias_generator=alias_reverse_generator,
        validate_by_name=True
    )