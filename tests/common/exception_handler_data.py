from typing import Tuple
from django.http.request import HttpRequest

from rest_framework import views
from rest_framework.request import Request

from common.exception.app_exception import APIException, UnAuthorizedException
from common.exception.exception_handler import ExceptionContext
from common.request_response.api_response import FailureAPIResponse
from config.messages import messages

# API処理中に発生した例外, 例外時コンテキスト, 期待結果
ParamType = Tuple[APIException, ExceptionContext, FailureAPIResponse]

class DataHandleException:


    def _get_param(self, exception: APIException, context: ExceptionContext, expected: FailureAPIResponse) -> ParamType:
        return (
            exception,
            context,
            expected
        )

    def get_unauthorized_exception(self) -> ParamType:

        exception = UnAuthorizedException()
        context: ExceptionContext = {
            'view': views.APIView(),
            'args': ('',),
            'kwargs': {'key': 'value'},
            'request': Request(HttpRequest())
        }

        expected: FailureAPIResponse = {
            'body': {
                'message': messages['common']['error']['unauthorized']
            }
        }

        return self._get_param(exception, context, expected)


data_handle_exception = DataHandleException()