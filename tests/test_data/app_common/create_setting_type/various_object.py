from typing import TypedDict, List, Tuple, Any

TypeADMINUSERS = TypedDict("TypeADMINUSERS", { "name": str, "age": int })
TypeSetting = TypedDict("TypeSetting", { "ADMIN_USERS": List[TypeADMINUSERS], "ALLOWED_PORTS": Tuple[int, int, int], "IS_DEBUG": bool })

setting_dict: TypeSetting = {
    "ADMIN_USERS": [{'name': 'pompom-purin', 'age': 100}, {'name': 'django', 'age': 3}],
    "ALLOWED_PORTS": (80, 443, 8080),
    "IS_DEBUG": True,
}

def get_setting_dict() -> TypeSetting:
    return setting_dict