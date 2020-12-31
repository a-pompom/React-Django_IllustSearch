import pytest

from common.api_response import api_response_handler
from .api_response_data import *

class TestAPIResponse:

    class Test__render_to_success_response:

        def test__body_from_message(self):

            # GIVEN
            sut = api_response_handler
            message, body, expected = data_render_success_response.get_only_message()
            # WHEN
            actual = sut.render_to_success_response(message)
            # THEN
            assert actual == expected

        def test_response_from_body(self):

            # GIVEN
            sut = api_response_handler
            message, body, expected = data_render_success_response.get_response_with_body()
            # WHEN
            actual = sut.render_to_success_response(body=body)
            # THEN
            assert actual == expected

    class Test__render_to_error_response:

        @pytest.mark.parametrize(
            'params',
            [
                pytest.param(data_render_to_error_response.get_single_field_error(), id='single_field_error'),
                pytest.param(data_render_to_error_response.get_comma_separated_field_error(), id='comma_separated_field_error'),
                pytest.param(data_render_to_error_response.get_multiple_field_error(), id='multiple_field_error'),
            ]
        )
        def test__get_error_response(self, params: ParamErrorResponseType):
            # GIVEN
            sut = api_response_handler
            message, errors, expected = params
            # WHEN
            actual = sut.render_to_error_response(message, errors)
            # THEN
            assert actual == expected

    class Test__render_to_failure_response:
        
        def test__get_failure_response(self):

            # GIVEN
            sut = api_response_handler
            message, expected = data_render_to_failure_response.get_failure()
            # WHEN
            actual = sut.render_to_failure_response(message)
            # THEN
            assert actual == expected