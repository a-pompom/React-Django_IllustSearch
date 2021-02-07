from typing import Tuple, Callable
from django.http.request import HttpRequest
from rest_framework.request import Request

from app_login.models import User

# ユーザ名
ParamGetUser = str
# リクエスト, ユーザ名, 期待結果ユーザ取得
# DjangoのDBへアクセスする処理は、呼び出し元が「django_db」マーカーが付与されている場合に限定されているので、
# 期待結果ユーザは、匿名関数でラップ
ParamAuthenticate = Tuple[Request, str, Callable[[],User]]

MOCK_USER_UUID = 'b21cffa2-ca96-4521-a338-557092c89fb3'

class DataGetUser:

    def _get_params(self, username: str) -> ParamGetUser:

        return username

    def get_alpha_numeric_username(self) -> ParamGetUser:
        return self._get_params('A-pompom1234')

    def get_unicode_username(self) -> ParamGetUser:
        return self._get_params('ポムポム')

    def get_no_exists_username(self) -> ParamGetUser:
        return self._get_params('nobody')


class DataAuthenticate:

    def _get_params(self, username: str) -> ParamAuthenticate:

        return (
            Request(HttpRequest()),
            username,
            lambda: User.objects.get(username=username),
        )

    def get_user(self) -> ParamAuthenticate:

        return self._get_params('A-pompom1234')


data_get_user = DataGetUser()
data_authenticate = DataAuthenticate()