from typing import TypedDict

class TypeCommonErrorMessages(TypedDict):
    unauthorized: str

class TypeCommonMessages(TypedDict):
    error: TypeCommonErrorMessages



class TypeMessages(TypedDict):
    common: TypeCommonMessages