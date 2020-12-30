from typing import TypedDict, List, Tuple, Any

fruits = ["apple", "banana"]
user = {"name": "pompom", "age": 100}
def get_type_def():
    return [fruits, user]

# TYPE DEF HERE
TypeFruits = List[str]
TypeUser = TypedDict("TypeUser", { "name": str, "age": int })