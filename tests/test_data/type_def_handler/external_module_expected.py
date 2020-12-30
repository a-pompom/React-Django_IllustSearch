from typing import TypedDict, List, Tuple, Any

def get_type_def():
    from .test_module import user
    return [user]

# TYPE DEF HERE
TypeUser = TypedDict("TypeUser", { "username": str, "is_authenticated": bool })