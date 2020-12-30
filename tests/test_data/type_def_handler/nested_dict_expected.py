from typing import TypedDict, List, Tuple, Any

response = { "body": { "message": "success", "status_code": 200}, "has_error": False }
user = {"username": "pompom", "age": 100,} 
def get_type_def():
    return [response, user]

# TYPE DEF HERE
TypeBody = TypedDict("TypeBody", { "message": str, "status_code": int })
TypeResponse = TypedDict("TypeResponse", { "body": TypeBody, "has_error": bool })
TypeUser = TypedDict("TypeUser", { "username": str, "age": int })