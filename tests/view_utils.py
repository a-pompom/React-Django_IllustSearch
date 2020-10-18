from typing import List, Tuple

from django.db import models
from rest_framework.test import APIClient
from rest_framework.status import HTTP_401_UNAUTHORIZED

from common.custom_type import TypeAPIResponse
from config.messages import messages

class IPathAvailable:
    """ API Path取得処理を実装したインタフェース """
    def _get_path(self) -> str:
        raise NotImplementedError

class DataViewMixin(IPathAvailable):
    """ View用テストデータクラスで利用するミックスイン """

    # 前処理 テスト対象をDB上へ事前に登録
    def _setup_db(self, *models_list: List[models.Model]):
        for models in models_list:
            [model.save() for model in models]

    def get_unauthorized(self) -> Tuple[APIClient, str, TypeAPIResponse]:

        client = APIClient()
        expected: TypeAPIResponse = {
            'body': {
                'message': messages['common']['error']['unauthorized']
            }
        }

        return (
            client,
            self._get_path(),
            expected
        )

class TestView:
    """ View用の共通テスト処理を記述したクラス """

    def _get_test_data(self) -> DataViewMixin:
        raise NotImplementedError

    def run_tests(self):
        """ 共通テスト実行処理 サブクラスでテストメソッドを経由して呼ばれる 

        Example
        -------
        test_共通処理(self):
            super().run_tests()
        """

        self.未ログインユーザによるGETリクエストで401レスポンスが得られること()

    def 未ログインユーザによるGETリクエストで401レスポンスが得られること(self):

        # GIVEN
        client, path, expected = self._get_test_data().get_unauthorized()

        # WHEN
        actual = client.get(path)

        # THEN
        assert actual.status_code == HTTP_401_UNAUTHORIZED
        assert actual.data == expected