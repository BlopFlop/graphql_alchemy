from pydantic import BaseModel, Field


class GraphQlField(BaseModel):
    name: str

    def __str__(self) -> str:
        return self.name


class GraphQlModel(BaseModel):
    name: str
    fields: list["GraphQlField | GraphQlModel"] = Field(min_length=1)

    def __str__(self):
        model_fields = " ".join(str(field) for field in self.fields)
        return f"{self.name} {{{model_fields}}}"


class GraphQlTypeValue(BaseModel):
    type: type
    graph_type: str
