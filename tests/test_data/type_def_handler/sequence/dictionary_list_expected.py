from typing import TypedDict, List, Tuple, Any

users = [{"username": "pompom", "user_age": 100}, {"username": "purin", "user_age": 0}]
def get_type_def():
    return [users]

# TYPE DEF HERE
TypeUsernameUserAge = TypedDict("TypeUsernameUserAge", { "username": str, "user_age": int })
TypeUsers = List[TypeUsernameUserAge]