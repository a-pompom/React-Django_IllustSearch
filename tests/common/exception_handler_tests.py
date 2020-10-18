from rest_framework.status import HTTP_401_UNAUTHORIZED
from common.exception_handler import handle_exception

from .exception_handler_data import data_handle_exception

class TestExceptionHandler:
    """ API例外ハンドラのテストクラス
    """

    class TestHandleException:

        def test_UnAuthorizedExceptionから401レスポンスが得られること(self):

            sut = handle_exception
            exception, context, expected = data_handle_exception.get_unauthorized_exception()

            actual = sut(exception, context)

            assert actual.data == expected
            assert actual.status_code == HTTP_401_UNAUTHORIZED