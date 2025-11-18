from typing import Literal, Union, Optional
from uuid import UUID, uuid4

import pytest
from dataclasses import fields, field, dataclass

from src.types import GraphQlMethodType, GraphQlQuery
from src.converter import dataclass_ as dataclass_converter

from tests.fixtures.fuctions import normalize_graphql_query
from tests.fixtures.queries import fst_query, snd_query, third_query, fouth_query


@dataclass
class ReturnError:
    typename: Literal["ReturnError"] = "ReturnError"
    message: str = "test"
    name: str = "test"


@dataclass
class Fst:
    typename: str = "TestModel"
    simple: str = "test"


@dataclass
class Snd:
    typename: Literal["Snd"] = "Snd"
    simple: str = "str"
    integer: int = 1
    uuid_: UUID = uuid4()
    float_: float = 1.0
    boolean: bool = True
    list_: list = field(default_factory=list)


@dataclass
class ThirdInput:
    project_id: int


third_input = ThirdInput(project_id=123)


@dataclass
class Thd:
    typename: Literal["TestModel"] = "TestModel"
    is_show_start: str = "test"
    is_check_sound: int = 1
    is_check_video: float = 2
    is_check_age: UUID = uuid4()
    is_check_sex: list = field(default_factory=list)
    if_double_cookie: dict = field(default_factory=dict)
    if_desktop: set = field(default_factory=set)
    if_mobile: int = 1
    is_asking_mark: Optional["Thd"] = None


# Вложенные модели
@dataclass
class City:
    city: str
    city_code: str
    city_id: int
    population: int


@dataclass
class ResearchCalcToCities:
    city_id: int
    city: City
    research_calc_uid: UUID


@dataclass
class Sex:
    sex: str
    sex_id: int
    sex_multiple: bool


@dataclass
class ResearchCalcToSexes:
    research_calc_uid: UUID
    sex: Sex
    sex_id: int


@dataclass
class Duration:
    duration: int
    duration_cost: float
    duration_id: int
    duration_lim: int


@dataclass
class ResearchCalc:
    age_max: int
    age_min: int
    count_respondent: int
    duration: Duration
    duration_id: int
    geo_id: int
    is_programming_form: bool
    is_use_quota: bool
    reachability: float
    research_calc_to_cities: list[ResearchCalcToCities]
    research_calc_to_sexes: list[ResearchCalcToSexes]
    research_calc_uid: UUID


@dataclass
class StatementAnswer:
    has_difficult_answer: bool
    is_fixed: bool
    sa_text: str
    sa_position: int
    sa_uid: UUID
    type_sa: str


@dataclass
class AdditionalQuestion:
    answer_order: int
    image_url: str
    max_selections: int
    max_value: int
    min_selections: int
    min_value: int
    question_position: int
    question_uid: UUID
    question_text: str
    statement_answer: StatementAnswer
    type_question: str
    statement_order: int


@dataclass
class Client:
    change_date: str
    company: str
    email: str
    first_name: str
    is_pdn: bool
    is_use: bool
    job_title: str
    last_name: str
    middle_name: str
    phone: str
    profile_uid: UUID
    profile_status_code: str
    registration_date: str


@dataclass
class ErrorComment:
    status: str
    text: str


@dataclass
class Feedback:
    comment: str
    feedback_id: UUID
    mark: int


@dataclass
class Questionnaire:
    file_id: UUID
    file_link: str
    file_name_from_user: str


@dataclass
class Quota:
    file_id: UUID
    file_link: str
    file_name_from_user: str


@dataclass
class ReportFile:
    link: str
    status: str


@dataclass
class CellsToQuotas:
    cell_uid: UUID
    research_quota_uid: UUID


@dataclass
class QuotaCell:
    cell_uid: UUID
    cell_id: int
    matrix_id: int
    matrix_respondents: int


@dataclass
class ResearchQuotas:
    dimension_id: int
    option_codes: str
    question_code: str
    research_quota_uid: UUID
    variable_id: int


@dataclass
class ResearchRedirect:
    redirect_uid: UUID
    redirect_status: str


@dataclass
class ResearchIntegration:
    cells_to_quotas: list[CellsToQuotas]
    main_matrix: str
    quota_cell: list[QuotaCell]
    research_duration: int
    research_priority: int
    research_quotas: list[ResearchQuotas]
    research_reachability: float
    research_redirect: list[ResearchRedirect]


@dataclass
class ResearchQuestions:
    question_id: int
    answer_id: int


@dataclass
class ResearchQuotasQuickCalc:
    count_respondents: int
    int_range: str
    option_codes: str
    panels_info: str
    percent: float
    question_code: str
    research_quota_uid: UUID


@dataclass
class ResearchQuickCalc:
    category_id: int
    cell_selection: str
    quantity: int
    research_questions: list[ResearchQuestions]
    research_quotas: list[ResearchQuotasQuickCalc]
    testing_type: str


@dataclass
class ResearchAttachments:
    research_uid: UUID
    attachment_uid: UUID
    attachment_type: str
    attachment_rules: str
    attachment_link_2: str
    attachment_data: str
    attachment_link_1: str


@dataclass
class ResearchQuickSolution:
    additional_questions_tab_count: int
    category_id: int
    cell_selection: str
    duration_id: int
    has_brand: bool
    has_price: bool
    ideas_text: str
    is_using_logo: bool
    product_launch_type: str
    purchase_period_type: str
    qma_integration_error: str
    quantity: int
    qma_updated: bool
    reachability: float
    research_attachments: list[ResearchAttachments]
    research_short_link: str
    research_uid: UUID
    testing_material_type: str
    tested_subject: str
    testing_type: str


# Основная модель для Research
@dataclass
class Research:
    bc_number: str
    client_profile_uid: UUID
    comment: str
    contract_num: str
    client: Client
    additional_question: list[AdditionalQuestion]
    date_change_status: str
    date_create: str
    date_edit: str
    date_end: str
    date_end_field: str
    date_report: str
    date_start_field: str
    date_start: str
    error_comment: ErrorComment
    feedback: Feedback
    is_upload_quota: bool
    link_form: str
    manager_cost: float
    platform: str
    project_comment: str
    project_manager: str
    questionnaire: Questionnaire
    quota: Quota
    reason_of_cancel: str
    reason_of_pause: str
    research_calc: ResearchCalc
    report_file: ReportFile
    research_cost: float
    research_count_respondent: int
    research_count_answer: int
    research_integration: ResearchIntegration
    research_name: str
    research_quick_calc: ResearchQuickCalc
    research_quick_solution: Union[ResearchQuickSolution, dict]
    research_status_code: str
    research_type: str
    research_uid: UUID
    type_contract_code: str


# Модель для пагинации
@dataclass
class ResearchPagination:
    typename: Literal["ResearchPagination"] = "ResearchPagination"
    researches: Union[list[Research], None] = None
    pages: int = 1


@dataclass
class Filter:
    pass


@dataclass
class OrderBy:
    pass


# Модель для входных параметров
@dataclass
class FourthInput:
    where: Optional[Filter] = None
    page: Optional[int] = None
    order_by: Optional[dict | OrderBy] = None
    limit: Optional[int] = None
    list_: Optional[list] = None


fourth_input = FourthInput(
    where=Filter(),
    page=1,
    order_by=OrderBy(),
    limit=10,
    list_=[]
)


@pytest.mark.parametrize(
    "schemas, inputs, check_query",
    (
        ((Fst, ReturnError), None, fst_query),
        ((Snd, ), None, snd_query),
        ((Thd, ReturnError, Thd), third_input, third_query),
        ((ResearchPagination, ReturnError), fourth_input, fouth_query),
    )
)
def test_build_query(schemas, inputs, check_query):
    inputs = (
        {field.name: getattr(inputs, field.name) for field in fields(inputs)}
        if inputs
        else
        None
    )
    query = GraphQlQuery(
        type_method=GraphQlMethodType.query,
        name="MyQuery",
        name_method="test_query",
        inputs=inputs,
        models=dataclass_converter.build_graph_ql_models(schemas),
    )
    assert normalize_graphql_query(str(query)) == normalize_graphql_query(check_query), f"{check_query} = {str(query)}"
