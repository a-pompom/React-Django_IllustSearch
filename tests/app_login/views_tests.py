import pytest

from django.urls import reverse_lazy

from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.response import Response
from typing import Dict, TypedDict

from .fixture import *

class Props(TypedDict):
    """ テストで利用するプロパティ型 """
    client: APIClient
    login_path: str
    sign_up_path: str
    top_path: str
    logout_path: str

# テストで利用するプロパティ生成
@pytest.fixture()
def props() -> Props:

    return {
        'client': APIClient(),
        'login_path': reverse_lazy('login:login'),
    }
@pytest.mark.django_db(transaction=False)
class TestLoginView:
    """ ログインAPIView """

    class TestGet:

        def get_response(self, props: Props) -> Response:
            """ GETリクエストを送信し、レスポンスを取得 """

            return props['client'].get(props['login_path'])

        """ ログインAPIへのGETリクエスト """
        def test_ステータス200が返ること(self, props: Props):

            # WHEN
            response = self.get_response(props)


            # THEN
            assert response.status_code == status.HTTP_200_OK

        def test_ユーザが空のときはデフォルトユーザが生成されレスポンスで渡されること(self, props: Props):

            # WHEN
            response = self.get_response(props)

            # THEN
            assert response.data[0]['username'] == 'user'

        def test_ユーザがすでに存在するときはデフォルトユーザが生成されないこと(self, props: Props, multiple_users):

            # WHEN
            response = self.get_response(props)

            # THEN
            assert {'username': 'user'} not in response.data

    class TestPost:

        def get_response(self, props: Props, params: Dict) -> Response:
            """ POSTリクエストを送信し、レスポンスを取得 """

            return props['client'].post(props['login_path'], params)

        def test_ログインに成功するとステータスコード200が返ること(self, props: Props, multiple_users):

            # GIVEN
            post_params = {
                'username': 'a-pompom0107',
            }

            # WHEN
            response = self.get_response(props, post_params)

            # THEN
            assert response.status_code == status.HTTP_200_OK

        def  test_ログインに失敗するとステータスコード401が返ること(self, props: Props, multiple_users):

            # GIVEN
            post_params = {
                'username': 'unknown user',
            }

            # WHEN
            response = self.get_response(props, post_params)

            # THEN
            assert response.status_code == status.HTTP_401_UNAUTHORIZED