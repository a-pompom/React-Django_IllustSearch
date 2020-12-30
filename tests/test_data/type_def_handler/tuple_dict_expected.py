from typing import TypedDict, List, Tuple, Any

user = {"username": "pompom", "tel": ("000-0000", "123-4567")}
characters_dict = {"characters": ({"name": "purin", "has_twitter_acount": False,}, {"name": "kitty", "has_twitter_acount": True,})}
def get_type_def():
    return [user, characters_dict]

# TYPE DEF HERE
TypeUser = TypedDict("TypeUser", { "username": str, "tel": Tuple[str, str] })
TypeCharacters = TypedDict("TypeCharacters", { "name": str, "has_twitter_acount": bool })
TypeCharactersDict = TypedDict("TypeCharactersDict", { "characters": Tuple[TypeCharacters, TypeCharacters] })