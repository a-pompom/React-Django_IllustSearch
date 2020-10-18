from common.custom_type import TypeAPIResponse
from typing import Tuple
from django.http.request import HttpRequest

from rest_framework import views
from rest_framework.request import Request

from common.exception_handler import APIException, TypeExceptionContext, UnAuthorizedException
from config.messages import messages


class DataHandleException:

    # API処理中に発生した例外, 例外時コンテキスト, 期待結果
    ParamType = Tuple[APIException, TypeExceptionContext, TypeAPIResponse]

    def _get_param(self, exception: APIException, context: TypeExceptionContext, expected: TypeAPIResponse) -> ParamType:
        return (
            exception,
            context,
            expected
        )

    def get_unauthorized_exception(self) -> ParamType:

        exception = UnAuthorizedException()
        context: TypeExceptionContext = {
            'view': views.APIView(),
            'args': ('',),
            'kwargs': {'key': 'value'},
            'request': Request(HttpRequest())
        }

        expected: TypeAPIResponse = {
            'body': {
                'message': messages['common']['error']['unauthorized']
            }
        }

        return self._get_param(exception, context, expected)

data_handle_exception = DataHandleException()