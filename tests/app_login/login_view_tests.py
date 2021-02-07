import pytest

from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED
from .login_view_data import data_login_view

from tests.view_utils import ParamViewRequestType, VIEW_REQUEST_PARAMS


@pytest.mark.django_db(transaction=False)
class TestLoginView:

    class Test__get:

        def test__get_default_user(self):
            # GIVEN
            param = data_login_view.get_default_user()
            # WHEN
            actual = param.client.get(param.path)
            # THEN
            assert actual.status_code == HTTP_200_OK
            assert actual.data == param.expected_response

        @pytest.mark.parametrize(
            VIEW_REQUEST_PARAMS,
            [
                pytest.param(data_login_view.get_users())
            ],
            indirect=[VIEW_REQUEST_PARAMS]
        )
        def test__get_users(self, view_request_params: ParamViewRequestType):
            # GIVEN
            param = view_request_params
            # WHEN
            actual = param.client.get(param.path)
            # THEN
            assert actual.status_code == HTTP_200_OK
            assert actual.data == param.expected_response

        @pytest.mark.parametrize(
            VIEW_REQUEST_PARAMS,
            [
                pytest.param(data_login_view.get_success_login())
            ],
            indirect=[VIEW_REQUEST_PARAMS]
        )
        def test__success_login(self, view_request_params: ParamViewRequestType):
            # GIVEN
            param = view_request_params
            # WHEN
            actual = param.client.post(param.path, param.post_body)
            # THEN
            assert actual.status_code == HTTP_200_OK
            assert actual.data == param.expected_response

        @pytest.mark.parametrize(
            VIEW_REQUEST_PARAMS,
            [pytest.param(data_login_view.get_failure_login())],
            indirect=[VIEW_REQUEST_PARAMS]
        )
        def test__failure_login(self, view_request_params: ParamViewRequestType):
            # GIVEN
            param = view_request_params
            # WHEN
            actual = param.client.post(param.path, param.post_body)
            # THEN
            assert actual.status_code == HTTP_401_UNAUTHORIZED
            assert actual.data == param.expected_response