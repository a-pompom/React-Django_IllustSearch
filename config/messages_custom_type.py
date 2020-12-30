from typing import TypedDict, List, Tuple, Any

def get_type_def():
    from .messages import messages
    return [messages]

# TYPE DEF HERE
TypeError = TypedDict("TypeError", { "unauthorized": str })
TypeCommon = TypedDict("TypeCommon", { "error": TypeError })
TypeMessages = TypedDict("TypeMessages", { "common": TypeCommon })