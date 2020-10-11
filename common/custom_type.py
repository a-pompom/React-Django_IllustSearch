from typing import Callable, TypeVar, TypedDict, Optional, List, Dict, Any, Generic, Union

from rest_framework.exceptions import ErrorDetail
from rest_framework.request import Request

# シリアライザに格納されたエラーオブジェクト
TypeSerializerErrorDict = Dict[str, List[ErrorDetail]]

class TypeErrorDict(TypedDict):
    """ エラーオブジェクト """
    fieldName: str
    message: str


class TypeAPIResponse(TypedDict, total=False):
    """ APIレスポンス """

    body: Optional[Dict[str, Any]]
    errors: Optional[List[TypeErrorDict]]

class TypeLoginUserHandler(TypedDict):
    """ ログインユーザハンドラ """
    get_login_user_id: Callable[[Request], Union[None, int]]