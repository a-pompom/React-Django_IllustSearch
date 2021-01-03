import pytest
from rest_framework.status import HTTP_200_OK

from .views_data import data_category_view
from tests.view_utils import test_common_view_function
from tests.conftest import ParamViewRequestType


@pytest.mark.django_db(transaction=False)
class TestCategoryView:

    def test__common(self):
        test_common_view_function.run_tests({'login_path': data_category_view.get_path()})

    class Test__get:

        @pytest.mark.parametrize(
            'view_request_params',
            [
                pytest.param(data_category_view.get_success_get(), id='simple')
            ],
            indirect=['view_request_params']
        )
        def test__get_categories(self, view_request_params: ParamViewRequestType):

            # GIVEN
            client, path, username, model_items_list, expected = view_request_params
            # WHEN
            client.login(username=username)
            actual = client.get(path)
            # THEN
            assert actual.status_code == HTTP_200_OK
            assert actual.data == expected


# @pytest.mark.django_db(transaction=False)
# class TestIllustView(TestView):

#     def _get_test_data(self):
#         return data_illust_view
    
#     def test_共通処理(self):
#         super().run_tests()

#     class TestGet:

#         def test_ログイン済ユーザによるGETリクエストでログインユーザのイラスト一覧が取得できること(self):

#             # GIVEN
#             client, path, username, expected = data_illust_view.get_success_get()

#             # WHEN
#             client.login(username=username)
#             actual = client.get(path)

#             assert actual.status_code == HTTP_200_OK
#             assert actual.data == expected