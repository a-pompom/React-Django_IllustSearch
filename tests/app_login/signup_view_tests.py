import pytest
from rest_framework.status import HTTP_200_OK, HTTP_422_UNPROCESSABLE_ENTITY

from .signup_view_data import data_signup_view
from tests.view_utils import ParamViewRequestType, VIEW_REQUEST_PARAMS

@pytest.mark.django_db(transaction=False)
class TestASignupView:

    class Test__post:

        def test__success_post(self):
            # GIVEN
            param: ParamViewRequestType = data_signup_view.get_success_post()
            # WHEN
            actual = param.client.post(param.path, param.post_body)
            # THEN
            assert actual.status_code == HTTP_200_OK
            assert actual.data == param.expected_response

        def test__failure_post_for_too_long_username(self):
            # GIVEN
            param: ParamViewRequestType = data_signup_view.get_too_long_username()
            # WHEN
            actual = param.client.post(param.path, param.post_body)
            # THEN
            assert actual.status_code == HTTP_422_UNPROCESSABLE_ENTITY
            assert actual.data == param.expected_response

        @pytest.mark.parametrize(
            VIEW_REQUEST_PARAMS,
            [
                pytest.param(data_signup_view.get_user_duplicate() ,id='simple')
            ],
            indirect=[VIEW_REQUEST_PARAMS]
        )
        def test__failure_post_for_duplicate_user(self, view_request_params: ParamViewRequestType):
            # GIVEN
            param = view_request_params
            # WHEN
            actual = param.client.post(param.path, param.post_body)
            # THEN
            assert actual.status_code == HTTP_422_UNPROCESSABLE_ENTITY
            assert actual.data == param.expected_response