fst_query = """
query MyQuery {
    test_query {
        ... on TestModel {
            __typename
            simple
        }
        ... on ReturnError {
            __typename
            message
            name
        }
    }
}
"""

snd_query = """
query MyQuery {
    test_query {
        ... on Snd {
            __typename
            simple
            integer
            uuid_
            float_
            boolean
            list_
        }
    }
}
"""


third_query = """
query MyQuery($project_id: Int) {
    test_query(project_id: $project_id) {
        ... on TestModel {
            __typename
            is_show_start
            is_check_sound
            is_check_video
            is_check_age
            is_check_sex
            if_double_cookie
            if_desktop
            if_mobile
            is_asking_mark
        }
        ... on ReturnError {
            __typename
            message
            name
        }
        ... on TestModel {
            __typename
            is_show_start
            is_check_sound
            is_check_video
            is_check_age
            is_check_sex
            if_double_cookie
            if_desktop
            if_mobile
            is_asking_mark
        }
    }
}
"""

fouth_query = """
query MyQuery($where: Filter, $page: Int, $order_by: OrderBy, $limit: Int) {
  test_query(where: $where, page: $page, order_by: $order_by, limit: $limit) {
    ... on ResearchPagination {
      __typename
      researches {
        bc_number
        client_profile_uid
        comment
        contract_num
        client {
          change_date
          company
          email
          first_name
          is_pdn
          is_use
          job_title
          last_name
          middle_name
          phone
          profile_uid
          profile_status_code
          registration_date
        }
        additional_question {
          answer_order
          image_url
          max_selections
          max_value
          min_selections
          min_value
          question_position
          question_uid
          question_text
          statement_answer {
            has_difficult_answer
            is_fixed
            sa_text
            sa_position
            sa_uid
            type_sa
          }
          type_question
          statement_order
        }
        date_change_status
        date_create
        date_edit
        date_end
        date_end_field
        date_report
        date_start_field
        date_start
        error_comment {
          status
          text
        }
        feedback {
          comment
          feedback_id
          mark
        }
        is_upload_quota
        link_form
        manager_cost
        platform
        project_comment
        project_manager
        questionnaire {
          file_id
          file_link
          file_name_from_user
        }
        quota {
          file_id
          file_link
          file_name_from_user
        }
        reason_of_cancel
        reason_of_pause
        research_calc {
          age_max
          age_min
          count_respondent
          duration {
            duration
            duration_cost
            duration_id
            duration_lim
          }
          duration_id
          geo_id
          is_programming_form
          is_use_quota
          reachability
          research_calc_to_cities {
            city_id
            city {
              city
              city_code
              city_id
              population
            }
            research_calc_uid
          }
          research_calc_to_sexes {
            research_calc_uid
            sex {
              sex
              sex_id
              sex_multiple
            }
            sex_id
          }
          research_calc_uid
        }
        report_file {
          link
          status
        }
        research_cost
        research_count_respondent
        research_count_answer
        research_integration {
          cells_to_quotas {
            cell_uid
            research_quota_uid
          }
          main_matrix
          quota_cell {
            cell_uid
            cell_id
            matrix_id
            matrix_respondents
          }
          research_duration
          research_priority
          research_quotas {
            dimension_id
            option_codes
            question_code
            research_quota_uid
            variable_id
          }
          research_reachability
          research_redirect {
            redirect_uid
            redirect_status
          }
        }
        research_name
        research_quick_calc {
          category_id
          cell_selection
          quantity
          research_questions {
            question_id
            answer_id
          }
          research_quotas {
            count_respondents
            int_range
            option_codes
            panels_info
            percent
            question_code
            research_quota_uid
          }
          testing_type
        }
        research_quick_solution {
          additional_questions_tab_count
          category_id
          cell_selection
          duration_id
          has_brand
          has_price
          ideas_text
          is_using_logo
          product_launch_type
          purchase_period_type
          qma_integration_error
          quantity
          qma_updated
          reachability
          research_attachments {
            research_uid
            attachment_uid
            attachment_type
            attachment_rules
            attachment_link_2
            attachment_data
            attachment_link_1
          }
          research_short_link
          research_uid
          testing_material_type
          tested_subject
          testing_type
        }
        research_status_code
        research_type
        research_uid
        type_contract_code
      }
      pages
    }
    ... on ReturnError {
      __typename
      message
      name
    }
  }
}
"""

