from typing import Tuple, List

from django.urls import reverse_lazy
from django.db import models
from rest_framework.test import APIClient

from app_illust_list.models import Category, Illust
from app_illust_list.serializers import CategorySerializer, IllustSerializer
from app_login.models import User

from common.custom_type import TypeAPIResponse
from tests.conftest import ParamViewRequestType

class DataCategoryView:

    def get_path(self) -> str:
        return reverse_lazy('illust_list:category')

    def _get_get_param(self, client: APIClient, login_username: str, model_items_list: List[List[models.Model]] ,  expected: TypeAPIResponse) -> ParamViewRequestType:
        return (
            client,
            self.get_path(),
            login_username,
            model_items_list,
            expected
        )

    def get_success_get(self) -> ParamViewRequestType:

        client = APIClient()
        login_username = 'ポムポム'

        # User
        user_login = User(pk=1, username=login_username)
        user_not_login = User(pk=2, username='purin')

        # Category
        category_list: List[models.Model] = [
            Category(user_id=user_login, category_name='写真'),
            Category(user_id=user_login, category_name='イラスト'),
            Category(user_id=user_not_login, category_name='イラスト'),
            Category(user_id=user_not_login, category_name='背景'),
        ]
        desc_order_category_list = [category_list[1], category_list[0]]

        expected: TypeAPIResponse = {
            'body': {
                'category_list': CategorySerializer(instance=desc_order_category_list, many=True).data
            }
        }

        return self._get_get_param(client, login_username, [[user_login, user_not_login], category_list], expected)

# class DataIllustView(DataViewMixin):

#     # リクエスト送信用APIクライアント, APIパス, ログインユーザ名, 期待結果
#     ParamType = Tuple[APIClient, str, str, TypeAPIResponse]

#     def _get_path(self) -> str:
#         return reverse_lazy('illust_list:illust_list')

#     def _get_get_param(self, client: APIClient, login_username: str, expected: TypeAPIResponse) -> ParamType:

#         return (
#             client,
#             self._get_path(),
#             login_username,
#             expected
#         )

#     def get_success_get(self) -> ParamType:

#         client = APIClient()
#         login_username = 'ポムポム'

#         # User
#         user_login = User(pk=1, username=login_username)
#         user_not_login = User(pk=2, username='purin')

#         # Illust
#         illust_list: List[models.Model] = [
#             Illust(user_id=user_login, path='/img/ポムポム/icon.png'),
#             Illust(user_id=user_login, path='/img/ポムポム/landscape/家.png'),
#             Illust(user_id=user_not_login, path='/img/purin/icon.png'),
#             Illust(user_id=user_not_login, path='/img/purin/写真_20200101.png'),
#         ]
#         desc_order_illust_list = [illust_list[1], illust_list[0]]

#         expected: TypeAPIResponse = {
#             'body': {
#                 'illust_list': IllustSerializer(instance=desc_order_illust_list, many=True).data
#             }
#         }

#         self._setup_db([user_login, user_not_login], illust_list)
#         client.login(username='ポムポム')

#         return self._get_get_param(client, login_username, expected)

data_category_view = DataCategoryView()
# data_illust_view = DataIllustView()