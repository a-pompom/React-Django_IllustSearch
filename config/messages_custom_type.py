from typing import TypedDict, List, Tuple, Any

def get_type_def():
    from .messages import messages
    return [messages]

# TYPE DEF HERE
TypeDelete = TypedDict("TypeDelete", { "invalid_uuid": str, "not_found": str })
TypeUpdate = TypedDict("TypeUpdate", { "invalid_uuid": str, "not_found": str })
TypeError = TypedDict("TypeError", { "update": TypeUpdate, "delete": TypeDelete })
TypeCategory = TypedDict("TypeCategory", { "error": TypeError })
TypeError = TypedDict("TypeError", { "unauthorized": str, "update_failure": str })
TypeSuccess = TypedDict("TypeSuccess", { "response_ok": str })
TypeCommon = TypedDict("TypeCommon", { "success": TypeSuccess, "error": TypeError })
TypeMessages = TypedDict("TypeMessages", { "common": TypeCommon, "category": TypeCategory })