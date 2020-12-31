from typing import Tuple, TypedDict, Dict, Any, Union
from rest_framework import views
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_401_UNAUTHORIZED

from .api_response import api_response_handler
from config.messages import messages

class APIException(Exception):
    """ API例外 """


class UnAuthorizedException(APIException):
    """ 未ログイン """


class TypeExceptionContext(TypedDict):
    """ 例外送出時点のViewコンテキスト """
    view: views.APIView
    args: Tuple[Any]
    kwargs: Dict[str, Any]
    request: Request


def handle_exception(exception: Exception, context: TypeExceptionContext) -> Union[Response, None]:
    """ 例外に応じたAPIResponseを生成

    Parameters
    ----------
    exception : Exception
        発生した例外と関連した例外クラスのインスタンス
    context : TypeExceptionContext
        例外発生時点のview・requestなどを格納したコンテキストオブジェクト

    Returns
    -------
    Union[Response, None]
        例外クラスに応じたAPIResponse
    """

    # 未ログイン
    if isinstance(exception, UnAuthorizedException):
        return Response(
            api_response_handler.render_to_failure_response(messages['common']['error']['unauthorized'])
            , status=HTTP_401_UNAUTHORIZED
        )