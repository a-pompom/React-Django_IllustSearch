from rest_framework.status import HTTP_401_UNAUTHORIZED
from common.exception.exception_handler import handle_exception

from .exception_handler_data import data_handle_exception

class TestExceptionHandler:

    class Test__handle_exception:

        def test__unauthorized_exception_response(self):

            # GIVEN
            sut = handle_exception
            exception, context, expected = data_handle_exception.get_unauthorized_exception()
            # WHEN
            actual = sut(exception, context)
            # THEN
            assert actual.data == expected
            assert actual.status_code == HTTP_401_UNAUTHORIZED