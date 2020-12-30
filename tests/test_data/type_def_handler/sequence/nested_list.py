from typing import TypedDict, List, Tuple, Any

address_list = [["Hiroshima-1-1", "Hiroshima-2-2"], ["Tokyo-0-0", "Tokyo-10-0"]]
def get_type_def():
    return [address_list]

# TYPE DEF HERE
TypeAddressList = List[List[str]]