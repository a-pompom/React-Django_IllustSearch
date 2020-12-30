from typing import TypedDict, List, Tuple, Any

TypeSetting = TypedDict("TypeSetting", { "VALUE": str })

setting_dict: TypeSetting = {
    "VALUE": 'value',
}

def get_setting_dict() -> TypeSetting:
    return setting_dict