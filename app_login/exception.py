from rest_framework.exceptions import ErrorDetail
from typing import Dict, List

class LoginFailureException(Exception):
    """ ログインに失敗したことを表す ログイン画面へと再度遷移させる """

    def __init__(self):
        self.errors: Dict[str, List[ErrorDetail]] = {'username': [ErrorDetail('ユーザ名が間違っています。')]}