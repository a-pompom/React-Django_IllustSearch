from typing import TypeVar, TypedDict, Optional, List, Dict, Any, Generic

from rest_framework.exceptions import ErrorDetail

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