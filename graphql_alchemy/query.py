from .types import InputGraphQlField, InputGraphQlModel, GraphQlModel, GraphQlField
from .enums import TypeMethod


def query(
    type: TypeMethod,
    name: str,
    inputs: list[InputGraphQlField | InputGraphQlModel] | None,
    models: list[GraphQlModel | GraphQlField],
    query_name: str = "Default",
) -> str:
    model_fields = " ".join(f"... on {str(model)}" for model in models)
    input_ = _input(inputs)
    method = f"{name}{input_} {{{model_fields}}}"
    return f"{type} {query_name} {{{method}}}"


def _input(inputs: list[InputGraphQlField | InputGraphQlModel]) -> str:
    if not inputs:
        return ""

    return "(" + " ".join(str(input_) for input_ in inputs) + ")"
