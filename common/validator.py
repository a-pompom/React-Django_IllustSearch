import re

def is_valid_min_length(value: str, length: int) -> bool:
    """ 最小文字数チェック
    Parameters
    ----------
    value : str
        検査対象文字列
    length : int
        許容される最小文字数
    Returns
    -------
    bool
        True -> 文字列が最小文字数以上
        False -> 文字列が最小文字数未満
    """

    if len(value) < length:
        return False

    return True

def is_valid_max_length(value: str, length: int) -> bool:
    """ 最大文字数チェック
    Parameters
    ----------
    value : str
        検査対象文字列
    length : int
        許容される最大文字数
    Returns
    -------
    bool
        True -> 文字列が最大文字数以下
        False -> 文字列が最大文字数より大きい
    """

    if len(value) > length:
        return False

    return True

def is_valid_alpha_numeric(value: str) -> bool:
    """ 文字列が半角英数と-_で構成されているか
    Parameters
    ----------
    value : str
        検査対象文字列
    Returns
    -------
    bool
        True -> 文字列が半角英数-_のみからなる
        False -> 文字列に半角英数-_以外が含まれる or 空文字
    """    

    return re.search('^[0-9a-zA-Z-_]+$', value) is not None