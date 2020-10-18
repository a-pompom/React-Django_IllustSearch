import pytest
from rest_framework.status import HTTP_200_OK

from .views_data import data_category_view, data_illust_view
from tests.view_utils import *


@pytest.mark.django_db(transaction=False)
class TestCategoryView(TestView):

    def _get_test_data(self):
        return data_category_view
    
    def test_共通処理(self):
        super().run_tests()

    class TestGet:

        def test_ログイン済ユーザによるGETリクエストでログインユーザのカテゴリ一覧が取得できること(self):

            # GIVEN
            client, path, username, expected = data_category_view.get_success_get()

            # WHEN
            client.login(username=username)
            actual = client.get(path)

            assert actual.status_code == HTTP_200_OK
            assert actual.data == expected


@pytest.mark.django_db(transaction=False)
class TestIllustView(TestView):

    def _get_test_data(self):
        return data_illust_view
    
    def test_共通処理(self):
        super().run_tests()

    class TestGet:

        def test_ログイン済ユーザによるGETリクエストでログインユーザのイラスト一覧が取得できること(self):

            # GIVEN
            client, path, username, expected = data_illust_view.get_success_get()

            # WHEN
            client.login(username=username)
            actual = client.get(path)

            assert actual.status_code == HTTP_200_OK
            assert actual.data == expected