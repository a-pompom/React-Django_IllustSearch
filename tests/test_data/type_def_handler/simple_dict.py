from typing import TypedDict, List, Tuple, Any

user = {"username": "pompom"}
def get_type_def():
    return [user]

# TYPE DEF HERE
TypeUser = TypedDict("TypeUser", { "username": str })