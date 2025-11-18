from datetime import date, datetime
from uuid import UUID

import pytest

from src import types, const
from tests.fixtures.fuctions import normalize_graphql_query


fst_mutation = """
mutation MyMutation {
  add_research {
    ... on ReturnError {
      __typename
      name
      message
    }
    ... on research {
      research_uid
      research_name
    }
  }
}
"""
fst_query = types.GraphQlQuery(
    type_method=types.GraphQlMethodType.mutation,
    name="MyMutation",
    name_method="add_research",
    models=[
        const.RETURN_ERROR,
        types.GraphQlModel(
            name="research", fields=[
                types.GraphQlField(name="research_uid"),
                types.GraphQlField(name="research_name"),
            ]
        )
    ]
)
snd_query_ = """
query MyMutation($comment: String, $date_end: Date) {
  add_research(comment: $comment, date_end: $date_end) {
    ... on ReturnError {
      __typename
      name
      message
    }
    ... on research {
      research_uid
      research_name
    }
  }
}
"""
snd_query = types.GraphQlQuery(
    type_method=types.GraphQlMethodType.query,
    name="MyMutation",
    name_method="add_research",
    inputs={"comment": "test", "date_end": date(2022, 1, 1)},
    models=[
        const.RETURN_ERROR,
        types.GraphQlModel(
            name="research", fields=[
                types.GraphQlField(name="research_uid"),
                types.GraphQlField(name="research_name"),
            ]
        )
    ]
)

thd_mutation = """
mutation MyMutation($comment: String, $date_end: Date, $type_contract_code: TypeContractCode) {
  add_research(comment: $comment, date_end: $date_end, type_contract_code: $type_contract_code) {
    ... on ReturnError {
      __typename
      name
      message
    }
    ... on research {
      research_uid
      research_name
    }
  }
}
"""


class TypeContractCode:
    pass


thd_query = types.GraphQlQuery(
    type_method=types.GraphQlMethodType.mutation,
    name="MyMutation",
    name_method="add_research",
    inputs={
        "comment": "test",
        "date_end": date(2022, 1, 1),
        "type_contract_code": TypeContractCode(),
    },
    models=[
        const.RETURN_ERROR,
        types.GraphQlModel(
            name="research", fields=[
                types.GraphQlField(name="research_uid"),
                types.GraphQlField(name="research_name"),
            ]
        )
    ]
)
foth_mutation = """
mutation MyMutation($research_calc: ResearchCalcInput) {
  add_research(research_calc: $research_calc) {
    ... on ReturnError {
      __typename
      name
      message
    }
    ... on research {
      research_uid
      research_name
    }
  }
}
"""


class ResearchCalcInput:
    pass


foth_query = types.GraphQlQuery(
    type_method=types.GraphQlMethodType.mutation,
    name="MyMutation",
    name_method="add_research",
    inputs={"research_calc": ResearchCalcInput()},
    models=[
        const.RETURN_ERROR,
        types.GraphQlModel(
            name="research", fields=[
                types.GraphQlField(name="research_uid"),
                types.GraphQlField(name="research_name"),
            ]
        )
    ]
)
six_mutation = """
mutation MyMutation {
    add_research {
        ... on ReturnError {
            __typename
            name
            message
        }
        ... on research {
            research_uid
            research_name
            research_quick_calc {
                category_id
                research_questions {
                    answer_id
                }
                research_quotas {
                    count_respondents
                }
            testing_type
            }
        }
    }
}"""
six_query = types.GraphQlQuery(
    type_method=types.GraphQlMethodType.mutation,
    name="MyMutation",
    name_method="add_research",
    models=[
        const.RETURN_ERROR,
        types.GraphQlModel(
            name="research", fields=[
                types.GraphQlField(name="research_uid"),
                types.GraphQlField(name="research_name"),
                types.GraphQlModel(
                    name="research_quick_calc",
                    fields=[
                        types.GraphQlField(name="category_id"),
                        types.GraphQlModel(name="research_questions", fields=[
                            types.GraphQlField(name="answer_id"),
                        ]),
                        types.GraphQlModel(name="research_quotas", fields=[
                            types.GraphQlField(name="count_respondents"),
                        ]),
                        types.GraphQlField(name="testing_type"),
                    ]
                )
            ]
        )
    ]
)

empty_inputs_mutation = """
query GetAll {
    get_all {
        ... on ReturnError {
            __typename
            name
            message
        }
        ... on model1 {
            field1
            field2
        }
        ... on model2 {
            field3
            field4
        }
        ... on model3 {
            field5
        }
    }
}
"""
empty_inputs_query = types.GraphQlQuery(
    type_method=types.GraphQlMethodType.query,
    name="GetAll",
    name_method="get_all",
    inputs=None,
    models=[
        const.RETURN_ERROR,
        types.GraphQlModel(
            name="model1",
            fields=[
                types.GraphQlField(name="field1"),
                types.GraphQlField(name="field2"),
            ]
        ),
        types.GraphQlModel(
            name="model2",
            fields=[
                types.GraphQlField(name="field3"),
                types.GraphQlField(name="field4"),
            ]
        ),
        types.GraphQlModel(
            name="model3",
            fields=[
                types.GraphQlField(name="field5"),
            ]
        )
    ]
)

special_chars_mutation = """query Research_Query_2023 {research_query_2023 {... on ReturnError {__typename name message} ... on research_data {data_id data_value}}}"""
special_chars_query = types.GraphQlQuery(
    type_method=types.GraphQlMethodType.query,
    name="Research_Query_2023",
    name_method="research_query_2023",
    models=[
        const.RETURN_ERROR,
        types.GraphQlModel(
            name="research_data",
            fields=[
                types.GraphQlField(name="data_id"),
                types.GraphQlField(name="data_value"),
            ]
        )
    ]
)

only_error_mutation = """mutation DeleteResearch {delete_research {... on ReturnError {__typename name message}}}"""
only_error_query = types.GraphQlQuery(
    type_method=types.GraphQlMethodType.mutation,
    name="DeleteResearch",
    name_method="delete_research",
    models=[
        const.RETURN_ERROR,
    ]
)

mixed_fields_mutation = """query GetResearchDetails {get_research_details {... on ReturnError {__typename name message} ... on research {simple_field research_details {detail_field deeper_details {deep_field}}}}}"""
mixed_fields_query = types.GraphQlQuery(
    type_method=types.GraphQlMethodType.query,
    name="GetResearchDetails",
    name_method="get_research_details",
    models=[
        const.RETURN_ERROR,
        types.GraphQlModel(
            name="research",
            fields=[
                types.GraphQlField(name="simple_field"),
                types.GraphQlModel(
                    name="research_details",
                    fields=[
                        types.GraphQlField(name="detail_field"),
                        types.GraphQlModel(
                            name="deeper_details",
                            fields=[
                                types.GraphQlField(name="deep_field"),
                            ]
                        ),
                    ]
                ),
            ]
        )
    ]
)


class MetadataInput:
    pass


complex_inputs_mutation = """
mutation ComplexMutation($id: UUID, $dates: [Date!], $metadata: MetadataInput) {
    complex_mutation(id: $id, dates: $dates, metadata: $metadata) {
        ... on ReturnError {
            __typename
            name
            message
        }
        ... on result {
            status
        }
    }
}
"""
complex_inputs_query = types.GraphQlQuery(
    type_method=types.GraphQlMethodType.mutation,
    name="ComplexMutation",
    name_method="complex_mutation",
    inputs={
        "id": UUID('11111111-2222-3333-4444-555555555555'),
        "dates": [date(2023, 1, 1), date(2023, 1, 2)],
        "metadata": MetadataInput(),
    },
    query_mapping_types={
        MetadataInput: "MetadataInput",
    },
    models=[
        const.RETURN_ERROR,
        types.GraphQlModel(
            name="result",
            fields=[
                types.GraphQlField(name="status"),
            ]
        )
    ]
)

deep_nested_mutation = """query GetResearch {get_research {... on ReturnError {__typename name message} ... on research {research_uid research_name researcher {researcher_id researcher_name contacts {email phone} department {department_name department_head {head_name}}}} ... on AdditionalModel {field1 field2}}}"""
deep_nested_query = types.GraphQlQuery(
    type_method=types.GraphQlMethodType.query,
    name="GetResearch",
    name_method="get_research",
    models=[
        const.RETURN_ERROR,
        types.GraphQlModel(
            name="research",
            fields=[
                types.GraphQlField(name="research_uid"),
                types.GraphQlField(name="research_name"),
                types.GraphQlModel(
                    name="researcher",
                    fields=[
                        types.GraphQlField(name="researcher_id"),
                        types.GraphQlField(name="researcher_name"),
                        types.GraphQlModel(
                            name="contacts",
                            fields=[
                                types.GraphQlField(name="email"),
                                types.GraphQlField(name="phone"),
                            ]
                        ),
                        types.GraphQlModel(
                            name="department",
                            fields=[
                                types.GraphQlField(name="department_name"),
                                types.GraphQlModel(
                                    name="department_head",
                                    fields=[
                                        types.GraphQlField(name="head_name"),
                                    ]
                                ),
                            ]
                        ),
                    ]
                ),
            ]
        ),
        types.GraphQlModel(
            name="AdditionalModel",
            fields=[
                types.GraphQlField(name="field1"),
                types.GraphQlField(name="field2"),
            ]
        )
    ]
)

uuid_datetime_mutation = """
mutation UpdateResearch($research_id: UUID, $updated_at: DateTime) {
    update_research(research_id: $research_id, updated_at: $updated_at) {
        ... on ReturnError {
            __typename
            name
            message
        }
        ... on research {
            research_uid
            research_name
        }
    }
}
"""
uuid_datetime_query = types.GraphQlQuery(
    type_method=types.GraphQlMethodType.mutation,
    name="UpdateResearch",
    name_method="update_research",
    inputs={
        "research_id": UUID('12345678-1234-5678-1234-567812345678'),
        "updated_at": datetime(2023, 12, 15, 10, 30, 0),
    },
    models=[
        const.RETURN_ERROR,
        types.GraphQlModel(
            name="research",
            fields=[
                types.GraphQlField(name="research_uid"),
                types.GraphQlField(name="research_name"),
            ]
        )
    ]
)
mixed_inputs_mutation = """
mutation CreateResearch($name: String, $budget: Float, $is_active: Boolean, $count: Int) {
    create_research(name: $name, budget: $budget, is_active: $is_active, count: $count) {
        ... on ReturnError {
            __typename
            name
            message
        }
        ... on research {
            research_uid
        }
    }
}
"""
mixed_inputs_query = types.GraphQlQuery(
    type_method=types.GraphQlMethodType.mutation,
    name="CreateResearch",
    name_method="create_research",
    inputs={
        "name": "Test Research",
        "budget": 150000.50,
        "is_active": True,
        "count": 100,
    },
    models=[
        const.RETURN_ERROR,
        types.GraphQlModel(
            name="research",
            fields=[
                types.GraphQlField(name="research_uid"),
            ]
        )
    ]
)


class CustomType:
    pass


class SpecialID:
    pass


custom_mapping_mutation = """
mutation SpecialMutation($custom_data: CustomType, $special_id: SpecialID) {
    special_method(custom_data: $custom_data, special_id: $special_id) {
        ... on ReturnError {
            __typename
            name
            message
        }
        ... on result {
            success
        }
    }
}
"""
custom_mapping_query = types.GraphQlQuery(
    type_method=types.GraphQlMethodType.mutation,
    name="SpecialMutation",
    name_method="special_method",
    inputs={
        "custom_data": CustomType(),
        "special_id": SpecialID(),
    },
    query_mapping_types={
        CustomType: "CustomType",
        SpecialID: "SpecialID",
    },
    models=[
        const.RETURN_ERROR,
        types.GraphQlModel(
            name="result",
            fields=[
                types.GraphQlField(name="success"),
            ]
        )
    ]
)


@pytest.mark.parametrize(
    "query_, check_query",
    (
        (fst_query, fst_mutation),
        (snd_query, snd_query_),
        (thd_query, thd_mutation),
        (foth_query, foth_mutation),
        (six_query, six_mutation),
        (uuid_datetime_query, uuid_datetime_mutation),
        (deep_nested_query, deep_nested_mutation),
        (mixed_inputs_query, mixed_inputs_mutation),
        (custom_mapping_query, custom_mapping_mutation),
        (empty_inputs_query, empty_inputs_mutation),
        (special_chars_query, special_chars_mutation),
        (only_error_query, only_error_mutation),
        (mixed_fields_query, mixed_fields_mutation),
        (complex_inputs_query, complex_inputs_mutation),
    )
)
def test_query_gen(query_: str, check_query: types.GraphQlQuery,):
    result = str(query_)
    assert normalize_graphql_query(check_query) == normalize_graphql_query(result), f"{check_query} = {result}"
