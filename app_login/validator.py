from rest_framework.exceptions import ValidationError
from typing import Dict

from common import validator
from .models import User

def clean_username(value_dict: Dict[str, str]) -> str:
    """ ユーザ名バリデーション
    文字種別・ユニークチェックを実行
    Returns
    -------
    value_dict: Dict[str, str]
        バリデーション後のユーザ名を格納した辞書
    Raise
    -----
    ValidationError
        文字長・ユニーク性を満たさなかったときに送出される
    """

    USERNAME_MAX_LENGTH = 255
    value: str = value_dict['username']

    if not value:
        return value

    # 文字長
    if not validator.is_valid_max_length(value, USERNAME_MAX_LENGTH):
        raise ValidationError(
            {
                'username': f'ユーザ名は{USERNAME_MAX_LENGTH}文字以下で入力してください。'
            }
        )

    # ユニーク
    if User.objects.filter(username=value).exists():
        raise ValidationError(
            {
                'username': f'ユーザ名はすでに使用されています。'
            }
        )

    return value