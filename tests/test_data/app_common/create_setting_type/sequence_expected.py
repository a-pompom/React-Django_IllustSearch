from typing import TypedDict, List, Tuple, Any

TypeSetting = TypedDict("TypeSetting", { "NAME_LIST": List[str] })

setting_dict: TypeSetting = {
    "NAME_LIST": ['pom', 'purin', 'john doe'],
}

def get_setting_dict() -> TypeSetting:
    return setting_dict