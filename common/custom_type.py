from typing import TypedDict, Optional, List, Dict

from rest_framework.exceptions import ErrorDetail

# シリアライザに格納されたエラーオブジェクト
TypeSerializerErrorDict = Dict[str, List[ErrorDetail]]

class TypePostErrorDict(TypedDict):
    """ エラーオブジェクト """
    fieldName: str
    message: str

class TypePostAPIResponse(TypedDict, total=False):
    """ POSTAPIレスポンス """

    message: str
    errors: Optional[List[TypePostErrorDict]]