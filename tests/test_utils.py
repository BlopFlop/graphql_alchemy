from datetime import date, datetime

import pytest

from src.utils import inputs_to_graphql_mapping
from src.const import String, Int, Float, Boolean


class TEST:
    pass


class TestContractInput:
    pass


class TESTScalar:
    pass


data_not_mapping_types_1 = {
    "research_calc": TEST(),
    "type_contract_code": TestContractInput(),
    "link_form": TESTScalar(),
}
check_types_1 = {"$research_calc: TEST!", "$type_contract_code: TestContractInput!", "$link_form: TESTScalar!"}
check_inputs_1 = {"research_calc: $research_calc", "type_contract_code: $type_contract_code", "link_form: $link_form"}

map_constant_type_2 = {
    **String.model_dump(),
    **Int.model_dump(),
    **Float.model_dump(),
    **Boolean.model_dump(),
}
data_constant_types_2 = {
    "string_type": "str",
    "int_type": 1,
    "float_type": 1.23,
    "boolean_type": True,
    "date_type": date(2020, 1, 1),
    "datetime_type": datetime(2020, 1, 1, 1, 1)
}
check_types_2 = {"$string_type: String!", "$int_type: Int!", "$float_type: Float!", "$boolean_type: Boolean!", "$date_type: Date!", "$datetime_type: DateTime!"}
check_inputs_2 = {"string_type: $string_type", "int_type: $int_type", "float_type: $float_type", "boolean_type: $boolean_type", "date_type: $date_type", "datetime_type: $datetime_type"}

map_empty_type_3 = {
    **String.model_dump(),
    **Int.model_dump(),
    **Float.model_dump(),
    **Boolean.model_dump(),
}
data_empty_types_3 = {}
check_empty_types_3 = {}
check_empty_inputs_3 = {}


@pytest.mark.parametrize(
    "data, mapping, check_types, check_inputs", (
        (data_not_mapping_types_1, dict(), check_types_1, check_inputs_1),
        (data_constant_types_2, map_constant_type_2, check_types_2, check_inputs_2),
        (data_empty_types_3, map_empty_type_3, check_empty_types_3, check_empty_inputs_3),
    )
)
def test_data_inputs_graphql(data, mapping, check_types, check_inputs):
    types, inputs = inputs_to_graphql_mapping(data, mapping)
    assert isinstance(types, str)
    assert isinstance(inputs, str)

    for type_ in check_types:
        assert type_ in check_types

    for input_ in check_inputs:
        assert input_ in check_inputs
