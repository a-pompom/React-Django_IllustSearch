import pytest

from common.api_response import api_response_handler as sut
from .api_response_data import *

class TestAPIResponse:

    class Test__Success:

        def test__render_message_only_response(self):
            # GIVEN
            message, body, expected = data_success.get_render()
            # WHEN
            actual = sut.success.render()
            # THEN
            assert actual.status_code == expected.status_code
            assert actual.data == expected.data
        
        def test__render_with_body(self):
            # GIVEN
            message, body, expected = data_success.get_render_with_body()
            # WHEN
            actual = sut.success.render_with_body(body)
            # THEN
            assert actual.status_code == expected.status_code
            assert actual.data == expected.data

        def test__render_with_updated_model(self):
            # GIVEN
            model_name, serializer, expected = data_success_update.get_render_with_updated_model()
            # WHEN
            actual = sut.success.render_with_updated_model(model_name, serializer)
            # THEN
            assert actual.status_code == expected.status_code
            assert actual.data == expected.data

    class Test__Failure:

        def test__unauthorized(self):
            # GIVEN
            expected = data_failure.get_unauthorized_error()
            # WHEN
            actual = sut.failure.render_unauthorized()
            # THEN
            assert actual.status_code == expected.status_code
            assert actual.data == expected.data
    

    class Test__FieldError:

        @pytest.mark.parametrize(
            'param', [
                pytest.param(data_field_error.get_single_field_error(), id='single_field'),
                pytest.param(data_field_error.get_comma_separated_field_error(), id='single_field_multiple_error'),
                pytest.param(data_field_error.get_multiple_field_error(), id='multiple_field'),
            ]
        )
        def test__field_error(self, param: FieldErrorParamType):
            # GIVEN
            expected, field_error = param
            # WHEN
            actual = sut.failure.render_field_error(field_error)
            # THEN
            assert actual.status_code == expected.status_code
            assert actual.data == expected.data