from typing import Literal, Union
from uuid import UUID

from src.types import GraphQlMethodType, GraphQlQuery

import pytest
from pydantic import BaseModel, Field

from src.converter import pydantic_ as pydantic_converter

from tests.fixtures.fuctions import normalize_graphql_query
from tests.fixtures.queries import fst_query, snd_query, third_query, fouth_query


class ReturnError(BaseModel):
    typename: Literal["ReturnError"] = Field(default="ReturnError", alias="__typename")
    message: str
    name: str


class Fst(BaseModel):
    typename: str = Field(default="TestModel", alias="__typename")
    simple: str


class Snd(BaseModel):
    typename: Literal["Snd"] = Field(default="Snd", alias="__typename")
    simple: str
    integer: int
    uuid_: UUID
    float_: float
    boolean: bool
    list_: list


class ThirdInput(BaseModel):
    project_id: int


third_input = ThirdInput(project_id=123)


class Thd(BaseModel):
    typename: Literal["TestModel"] = Field(default="TestModel", alias="__typename")
    is_show_start: str
    is_check_sound: int
    is_check_video: float
    is_check_age: UUID
    is_check_sex: list
    if_double_cookie: dict
    if_desktop: set
    if_mobile: int
    is_asking_mark: "Thd"


# Вложенные модели
class City(BaseModel):
    city: str
    city_code: str
    city_id: int
    population: int


class ResearchCalcToCities(BaseModel):
    city_id: int
    city: City
    research_calc_uid: UUID


class Sex(BaseModel):
    sex: str
    sex_id: int
    sex_multiple: bool


class ResearchCalcToSexes(BaseModel):
    research_calc_uid: UUID
    sex: Sex
    sex_id: int


class Duration(BaseModel):
    duration: int
    duration_cost: float
    duration_id: int
    duration_lim: int


class ResearchCalc(BaseModel):
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


class StatementAnswer(BaseModel):
    has_difficult_answer: bool
    is_fixed: bool
    sa_text: str
    sa_position: int
    sa_uid: UUID
    type_sa: str


class AdditionalQuestion(BaseModel):
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


class Client(BaseModel):
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


class ErrorComment(BaseModel):
    status: str
    text: str


class Feedback(BaseModel):
    comment: str
    feedback_id: UUID
    mark: int


class Questionnaire(BaseModel):
    file_id: UUID
    file_link: str
    file_name_from_user: str


class Quota(BaseModel):
    file_id: UUID
    file_link: str
    file_name_from_user: str


class ReportFile(BaseModel):
    link: str
    status: str


class CellsToQuotas(BaseModel):
    cell_uid: UUID
    research_quota_uid: UUID


class QuotaCell(BaseModel):
    cell_uid: UUID
    cell_id: int
    matrix_id: int
    matrix_respondents: int


class ResearchQuotas(BaseModel):
    dimension_id: int
    option_codes: str
    question_code: str
    research_quota_uid: UUID
    variable_id: int


class ResearchRedirect(BaseModel):
    redirect_uid: UUID
    redirect_status: str


class ResearchIntegration(BaseModel):
    cells_to_quotas: list[CellsToQuotas]
    main_matrix: str
    quota_cell: list[QuotaCell]
    research_duration: int
    research_priority: int
    research_quotas: list[ResearchQuotas]
    research_reachability: float
    research_redirect: list[ResearchRedirect]


class ResearchQuestions(BaseModel):
    question_id: int
    answer_id: int


class ResearchQuotasQuickCalc(BaseModel):
    count_respondents: int
    int_range: str
    option_codes: str
    panels_info: str
    percent: float
    question_code: str
    research_quota_uid: UUID


class ResearchQuickCalc(BaseModel):
    category_id: int
    cell_selection: str
    quantity: int
    research_questions: list[ResearchQuestions]
    research_quotas: list[ResearchQuotasQuickCalc]
    testing_type: str


class ResearchAttachments(BaseModel):
    research_uid: UUID
    attachment_uid: UUID
    attachment_type: str
    attachment_rules: str
    attachment_link_2: str
    attachment_data: str
    attachment_link_1: str


class ResearchQuickSolution(BaseModel):
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
class Research(BaseModel):
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
class ResearchPagination(BaseModel):
    typename: Literal["ResearchPagination"] = Field(default="ResearchPagination", alias="__typename")
    researches: list[Research]
    pages: int


class Filter(BaseModel):
    pass


class OrderBy(BaseModel):
    pass


# Модель для входных параметров
class FourthInput(BaseModel):
    where: Filter | None = None
    page: int | None = None
    order_by: dict | OrderBy | None = None
    limit: int | None = None
    list_: list | None = None


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
        {field: getattr(inputs, field) for field in inputs.model_dump().keys()}
        if inputs
        else
        None
    )
    query = GraphQlQuery(
        type_method=GraphQlMethodType.query,
        name="MyQuery",
        name_method="test_query",
        inputs=inputs,
        models=pydantic_converter.build_graph_ql_models(schemas),
    )
    assert normalize_graphql_query(str(query)) == normalize_graphql_query(check_query), f"{check_query} = {str(query)}"
