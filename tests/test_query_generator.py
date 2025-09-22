from enum import StrEnum
from datetime import date
from uuid import UUID

import pytest
from pydantic import BaseModel

from graphql_alchemy import enums, query, types, const


mutation_1 = """mutation MyMutation {add_research {... on research {comment bc_number client_profile_uid date_change_status} ... on ReturnError {__typename name message}}}"""
type_1 = enums.TypeMethod.mutation
name_1 = "add_research"
inputs_1 = None
models_1 = [
    types.GraphQlModel(
        name="research",
        fields=[
            types.GraphQlField(name="comment", type=str),
            types.GraphQlField(name="bc_number", type=int),
            types.GraphQlField(name="client_profile_uid", type=UUID),
            types.GraphQlField(name="date_change_status", type=date),
        ]
    ),
    const.RETURN_ERROR
]
method_name_1 = "MyMutation"

mutation_2 = """mutation MyMutation {update_research(research_calc: {count_respondent: 10.1, is_use_quota: use_quota_false, is_programming_form: false, test: true, research_calc_to_sexes: 10, list: [1, '2', 3, '4'], json: {'test1': 'dop', 'date_': '2020-01-01'}} comment: 'test' date_end: '2020-01-01' research_name: 'test' type_contract_code: usual_contract) {... on research {comment link_form research_calc {age_max duration {duration_id duration_lim}}}}}"""


class defalultEnum(StrEnum):
    usual_contract = "usual_contract"
    use_quota_false = "use_quota_false"


class DefaultJsonModel(BaseModel):
    test1: str = "dop"
    date_: date = date(2020, 1, 1)


type_2 = enums.TypeMethod.mutation
name_2 = "update_research"
inputs_2 = [
    types.InputGraphQlModel(
        name="research_calc",
        inputs=[
            types.InputGraphQlField(name="count_respondent", type=float, value=10.1),
            types.InputGraphQlField(name="is_use_quota", type=StrEnum, value=defalultEnum.use_quota_false),
            types.InputGraphQlField(name="is_programming_form", type=bool, value=False),
            types.InputGraphQlField(name="test", type=bool, value=True),
            types.InputGraphQlField(name="research_calc_to_sexes", type=int, value=10),
            types.InputGraphQlField(name="list", type=list, value=[1, "2", 3, "4"]),
            types.InputGraphQlField(name="json", type=dict, value=DefaultJsonModel().model_dump(mode="json")),
        ]
    ),
    types.InputGraphQlField(name="comment", type=str, value="test"),
    types.InputGraphQlField(name="date_end", type=date, value=date(2020, 1, 1)),
    types.InputGraphQlField(name="research_name", type=str, value="test"),
    types.InputGraphQlField(name="type_contract_code", type=StrEnum, value=defalultEnum.usual_contract),
]
models_2 = [
    types.GraphQlModel(
        name="research",
        fields=[
            types.GraphQlField(name="comment", type=str),
            types.GraphQlField(name="link_form", type=str),
            types.GraphQlModel(name="research_calc", fields=[
                types.GraphQlField(name="age_max", type=int),
                types.GraphQlModel(name="duration", fields=[
                    types.GraphQlField(name="duration_id", type=int),
                    types.GraphQlField(name="duration_lim", type=int)
                ])
            ])
        ]
    )
]
method_name_2 = "MyMutation"


query_3 = """query MyQuery {file_download(file_link: 'test') {... on FileDownload {__typename temp_url} ... on ReturnError {__typename name message}}}"""
name_3 = "file_download"
method_name_3 = "MyQuery"
inputs_3 = [types.InputGraphQlField(name="file_link", type=str, value="test")]
models_3 = [
    types.GraphQlModel(name="FileDownload", fields=[
        types.GraphQlField(name="__typename", type=str),
        types.GraphQlField(name="temp_url", type=str)
    ]),
    const.RETURN_ERROR
]

query_4 = """query MyQuery {research_name {... on ResearchName {__typename research_name} ... on ReturnError {__typename name message}}}"""
name_4 = "research_name"
method_name_4 = "MyQuery"
inputs_4 = None
models_4 = [
    types.GraphQlModel(name="ResearchName", fields=[
        types.GraphQlField(name="__typename", type=str),
        types.GraphQlField(name="research_name", type=str)
    ]),
    const.RETURN_ERROR
]


@pytest.mark.parametrize(
    "query, type, name, inputs, models, method_name",
    (
        (mutation_1, enums.TypeMethod.mutation, name_1, inputs_1, models_1, method_name_1),
        (mutation_2, enums.TypeMethod.mutation, name_2, inputs_2, models_2, method_name_2),
        (query_3, enums.TypeMethod.query, name_3, inputs_3, models_3, method_name_3),
        (query_4, enums.TypeMethod.query, name_4, inputs_4, models_4, method_name_4),
    )
)
def test_query_gen(
    query: str,
    type: enums.TypeMethod,
    name: str,
    inputs: list[types.InputGraphQlModel],
    models: list[types.GraphQlModel],
    method_name: str
):
    result = query.query(type, name, inputs, models, method_name)
    assert query == result, f"{result} != {query}"


def test_field_validation_error():
    with pytest.raises(TypeError):
        types.InputGraphQlField(name="test", type=BaseModel, value=10)
