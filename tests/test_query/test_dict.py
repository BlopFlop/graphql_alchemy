from src.types import GraphQlMethodType, GraphQlQuery
import pytest
from src.converter.dict_ import build_graph_ql_models
from tests.fixtures.fuctions import normalize_graphql_query
from tests.fixtures.queries import fst_query, snd_query, third_query, fouth_query

# Данные для тестов в виде словарей
return_error_data = {
    "__typename": "ReturnError",
    "message": "test_message",
    "name": "test_name"
}

fst_data = {
    "__typename": "TestModel",
    "simple": "test_string"
}

snd_data = {
    "__typename": "Snd",
    "simple": "test_string",
    "integer": 123,
    "uuid_": "12345678-1234-1234-1234-123456789012",
    "float_": 123.45,
    "boolean": True,
    "list_": ["item1", "item2"]
}

thd_data = {
    "__typename": "TestModel",
    "is_show_start": "test",
    "is_check_sound": 1,
    "is_check_video": 1.5,
    "is_check_age": "12345678-1234-1234-1234-123456789012",
    "is_check_sex": ["male", "female"],
    "if_double_cookie": [],
    "if_desktop": {},
    "if_mobile": 1,
    "is_asking_mark": "Nan",
}

# Сложные вложенные структуры для Research
city_data = {
    "city": "Moscow",
    "city_code": "MSK",
    "city_id": 1,
    "population": 12000000
}

research_calc_to_cities_data = {
    "city_id": 1,
    "city": city_data,
    "research_calc_uid": "12345678-1234-1234-1234-123456789012"
}

sex_data = {
    "sex": "male",
    "sex_id": 1,
    "sex_multiple": False
}

research_calc_to_sexes_data = {
    "research_calc_uid": "12345678-1234-1234-1234-123456789012",
    "sex": sex_data,
    "sex_id": 1
}

duration_data = {
    "duration": 30,
    "duration_cost": 100.0,
    "duration_id": 1,
    "duration_lim": 60
}

research_calc_data = {
    "age_max": 65,
    "age_min": 18,
    "count_respondent": 1000,
    "duration": duration_data,
    "duration_id": 1,
    "geo_id": 1,
    "is_programming_form": True,
    "is_use_quota": False,
    "reachability": 85.5,
    "research_calc_to_cities": [research_calc_to_cities_data],
    "research_calc_to_sexes": [research_calc_to_sexes_data],
    "research_calc_uid": "12345678-1234-1234-1234-123456789012"
}

statement_answer_data = {
    "has_difficult_answer": False,
    "is_fixed": True,
    "sa_text": "Answer text",
    "sa_position": 1,
    "sa_uid": "12345678-1234-1234-1234-123456789012",
    "type_sa": "single"
}

additional_question_data = {
    "answer_order": 1,
    "image_url": "http://example.com/image.jpg",
    "max_selections": 1,
    "max_value": 10,
    "min_selections": 1,
    "min_value": 1,
    "question_position": 1,
    "question_uid": "12345678-1234-1234-1234-123456789012",
    "question_text": "Question text",
    "statement_answer": statement_answer_data,
    "type_question": "single_choice",
    "statement_order": 1
}

client_data = {
    "change_date": "2023-01-01",
    "company": "Test Company",
    "email": "test@example.com",
    "first_name": "John",
    "is_pdn": False,
    "is_use": True,
    "job_title": "Manager",
    "last_name": "Doe",
    "middle_name": "Middle",
    "phone": "+1234567890",
    "profile_uid": "12345678-1234-1234-1234-123456789012",
    "profile_status_code": "active",
    "registration_date": "2023-01-01"
}

error_comment_data = {
    "status": "error",
    "text": "Error comment text"
}

feedback_data = {
    "comment": "Feedback comment",
    "feedback_id": "12345678-1234-1234-1234-123456789012",
    "mark": 5
}

questionnaire_data = {
    "file_id": "12345678-1234-1234-1234-123456789012",
    "file_link": "http://example.com/file.pdf",
    "file_name_from_user": "questionnaire.pdf"
}

quota_data = {
    "file_id": "12345678-1234-1234-1234-123456789012",
    "file_link": "http://example.com/quota.pdf",
    "file_name_from_user": "quota.pdf"
}

report_file_data = {
    "link": "http://example.com/report.pdf",
    "status": "completed"
}

cells_to_quotas_data = {
    "cell_uid": "12345678-1234-1234-1234-123456789012",
    "research_quota_uid": "12345678-1234-1234-1234-123456789012"
}

quota_cell_data = {
    "cell_uid": "12345678-1234-1234-1234-123456789012",
    "cell_id": 1,
    "matrix_id": 1,
    "matrix_respondents": 100
}

research_quotas_data = {
    "dimension_id": 1,
    "option_codes": "A,B,C",
    "question_code": "Q1",
    "research_quota_uid": "12345678-1234-1234-1234-123456789012",
    "variable_id": 1
}

research_redirect_data = {
    "redirect_uid": "12345678-1234-1234-1234-123456789012",
    "redirect_status": "active"
}

research_integration_data = {
    "cells_to_quotas": [cells_to_quotas_data],
    "main_matrix": "main",
    "quota_cell": [quota_cell_data],
    "research_duration": 30,
    "research_priority": 1,
    "research_quotas": [research_quotas_data],
    "research_reachability": 85.5,
    "research_redirect": [research_redirect_data]
}

research_questions_data = {
    "question_id": 1,
    "answer_id": 1
}

research_quotas_quick_calc_data = {
    "count_respondents": 1000,
    "int_range": "18-65",
    "option_codes": "A,B,C",
    "panels_info": "panel1,panel2",
    "percent": 85.5,
    "question_code": "Q1",
    "research_quota_uid": "12345678-1234-1234-1234-123456789012"
}

research_quick_calc_data = {
    "category_id": 1,
    "cell_selection": "random",
    "quantity": 1000,
    "research_questions": [research_questions_data],
    "research_quotas": [research_quotas_quick_calc_data],
    "testing_type": "standard"
}

research_attachments_data = {
    "research_uid": "12345678-1234-1234-1234-123456789012",
    "attachment_uid": "12345678-1234-1234-1234-123456789012",
    "attachment_type": "document",
    "attachment_rules": "rules",
    "attachment_link_2": "http://example.com/doc2.pdf",
    "attachment_data": "data",
    "attachment_link_1": "http://example.com/doc1.pdf"
}

research_quick_solution_data = {
    "additional_questions_tab_count": 2,
    "category_id": 1,
    "cell_selection": "random",
    "duration_id": 1,
    "has_brand": True,
    "has_price": True,
    "ideas_text": "Ideas text",
    "is_using_logo": True,
    "product_launch_type": "new",
    "purchase_period_type": "monthly",
    "qma_integration_error": "",
    "quantity": 1000,
    "qma_updated": True,
    "reachability": 85.5,
    "research_attachments": [research_attachments_data],
    "research_short_link": "http://short.link",
    "research_uid": "12345678-1234-1234-1234-123456789012",
    "testing_material_type": "standard",
    "tested_subject": "product",
    "testing_type": "standard"
}

research_data = {
    "bc_number": "BC123",
    "client_profile_uid": "12345678-1234-1234-1234-123456789012",
    "comment": "Research comment",
    "contract_num": "CONTRACT123",
    "client": client_data,
    "additional_question": [additional_question_data],
    "date_change_status": "2023-01-01",
    "date_create": "2023-01-01",
    "date_edit": "2023-01-01",
    "date_end": "2023-12-31",
    "date_end_field": "2023-12-31",
    "date_report": "2024-01-15",
    "date_start_field": "2023-01-01",
    "date_start": "2023-01-01",
    "error_comment": error_comment_data,
    "feedback": feedback_data,
    "is_upload_quota": True,
    "link_form": "http://example.com/form",
    "manager_cost": 5000.0,
    "platform": "web",
    "project_comment": "Project comment",
    "project_manager": "Manager Name",
    "questionnaire": questionnaire_data,
    "quota": quota_data,
    "reason_of_cancel": "",
    "reason_of_pause": "",
    "research_calc": research_calc_data,
    "report_file": report_file_data,
    "research_cost": 10000.0,
    "research_count_respondent": 1000,
    "research_count_answer": 950,
    "research_integration": research_integration_data,
    "research_name": "Test Research",
    "research_quick_calc": research_quick_calc_data,
    "research_quick_solution": research_quick_solution_data,
    "research_status_code": "active",
    "research_type": "standard",
    "research_uid": "12345678-1234-1234-1234-123456789012",
    "type_contract_code": "standard"
}

research_pagination_data = {
    "__typename": "ResearchPagination",
    "researches": [research_data],
    "pages": 5
}

# Input данные
third_input_data = {
    "project_id": 123
}


class Filter:
    pass


class OrderBy:
    pass


fourth_input_data = {
    "where": Filter(),
    "page": 1,
    "order_by": OrderBy(),
    "limit": 10,
    "list_": []
}


@pytest.mark.parametrize(
    "data_dicts, inputs, check_query",
    (
        ([fst_data, return_error_data], None, fst_query),
        ([snd_data], None, snd_query),
        ([thd_data, return_error_data, thd_data], third_input_data, third_query),
        ([research_pagination_data, return_error_data], fourth_input_data, fouth_query),
    )
)
def test_build_query_from_dict(data_dicts, inputs, check_query):
    query = GraphQlQuery(
        type_method=GraphQlMethodType.query,
        name="MyQuery",
        name_method="test_query",
        inputs=inputs,
        models=build_graph_ql_models(data_dicts),
    )
    assert normalize_graphql_query(str(query)) == normalize_graphql_query(check_query), f"{check_query} = {str(query)}"