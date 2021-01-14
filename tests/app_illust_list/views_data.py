from typing import Dict, Tuple, List, Optional, Any

from django.urls import reverse_lazy
from django.db import models
from rest_framework.test import APIClient

from app_illust_list.models import Category, Illust
from app_illust_list.serializers import CategorySerializer, IllustSerializer
from app_login.models import User

from common.custom_type import TypeAPIResponse
from tests.conftest import ParamViewRequestType

MOCK_CATEGORY_UUID_LIST = [
    'f503f432-7a5a-47e4-bc35-295f0fe2d853',
    '755ce7a0-dafb-46ef-a62f-c1c10e5fafd9',
    '1d16f05b-b3ad-4868-945a-a722de95439f',
    '42ca47c3-369b-4dd2-87ff-618f3d67cea0',
    '9a19af5a-3fe4-455c-9d00-74fa6d13b4e4',
    'f09e9c33-a999-4a42-b3a1-5d9447028c4e',
    '445e5b5d-8dcf-4393-93c1-1d435d38510d',
    'bc3a390a-b168-4f9b-b1b9-489d129f66d9',
    'a4c0158c-3cc0-4f40-9519-5f123b2ab799',
    '9ebff94e-a3df-4782-afca-fd62df59a408',
    'c5cd4d37-bf0d-4a59-9707-ef8a75dd1912',
]

class DataCategoryView:

    def get_path(self) -> str:
        return reverse_lazy('illust_list:category')

    def _get_param(
        self, 
        login_username: str, 
        model_items_list: List[List[models.Model]] ,
        expected: TypeAPIResponse,
        get_query: str = '',
        post_body: Dict[str, Any] = {},
        put_body: Dict[str, Any] = {},
        delete_body: Dict[str, Any] = {},
    ) -> ParamViewRequestType:

        return ParamViewRequestType(
            APIClient(),
            self.get_path(),
            login_username,
            model_items_list,
            expected,
            get_query,
            post_body,
            put_body,
            delete_body
        )

    def get_success_get(self) -> ParamViewRequestType:

        login_username = 'ポムポム'

        # Users
        user_login = User(pk=1, username=login_username)
        user_not_login = User(pk=2, username='purin')

        # Category
        category_list: List[models.Model] = [
            Category(category_id=MOCK_CATEGORY_UUID_LIST[0], user_id=user_login, category_name='写真', sort_order=1),
            Category(category_id=MOCK_CATEGORY_UUID_LIST[1], user_id=user_login, category_name='イラスト', sort_order=2),
            Category(category_id=MOCK_CATEGORY_UUID_LIST[2], user_id=user_not_login, category_name='イラスト', sort_order=1),
            Category(category_id=MOCK_CATEGORY_UUID_LIST[3], user_id=user_not_login, category_name='背景', sort_order=2),
        ]
        desc_order_category_list = [category_list[0], category_list[1]]

        expected: TypeAPIResponse = {
            'body': {
                'category_list': CategorySerializer(instance=desc_order_category_list, many=True).data
            }
        }

        return self._get_param(login_username, [[user_login, user_not_login], category_list], expected)

    def get_single_category(self):
        login_username = 'ポムポム'
        user_login = User(pk=1, username=login_username)
        post_body = {'category_name': '実写'}

        expected: TypeAPIResponse = {
            'body': {
                'category': {'category_id': MOCK_CATEGORY_UUID_LIST[0], 'category_name': '実写', 'user_id': 1, 'sort_order': 1}
            }
        }

        return self._get_param(login_username, [[user_login]], expected, post_body=post_body)

    def get_empty_category_post(self):
        login_username = 'ポムポム'
        user_login = User(pk=1, username=login_username)
        post_body = {'category_name': ''}

        expected: TypeAPIResponse = {
            'body': {
                'message': '登録に失敗しました。',
            },
            'errors': [
                {'fieldName': 'category_name', 'message': 'カテゴリ名を入力してください。'}
            ],
        }

        return self._get_param(login_username, [[user_login]], expected, post_body=post_body)

    def get_duplicate_category_post(self):
        login_username = 'ポムポム'
        user_login = User(pk=1, username=login_username)
        post_body = {'category_name': '実写'}

        expected: TypeAPIResponse = {
            'body': {
                'message': '登録に失敗しました。',
            },
            'errors': [
                {'fieldName': 'category_name', 'message': 'カテゴリ名は既に使用されています。'}
            ],
        }

        return self._get_param(login_username, [[user_login]], expected, post_body=post_body)

    def get_single_category_put(self):
        login_username = 'ポムポム'
        user_login = User(pk=1, username=login_username)
        post_body = {'category_name': '実写'}
        put_body = {'category_name': '実写画像', 'category_id': MOCK_CATEGORY_UUID_LIST[0]}

        expected: TypeAPIResponse = {
            'body': {
                'category': {'category_id': MOCK_CATEGORY_UUID_LIST[0], 'category_name': '実写画像', 'user_id': 1, 'sort_order': 1}
            }
        }

        return self._get_param(login_username, [[user_login]], expected, post_body=post_body, put_body=put_body)

    def get_empty_category_id_put(self):

        login_username = 'ポムポム'
        user_login = User(pk=1, username=login_username)
        post_body = {'category_name': '実写'}
        put_body= {'category_name': '実写映画', 'category_id': ''}

        expected: TypeAPIResponse = {
            'body': {
                'message': '登録に失敗しました。',
            },
            'errors': [
                {'fieldName': 'category_id', 'message': 'カテゴリIDはUUID形式で指定してください。'}
            ],
        }

        return self._get_param(login_username, [[user_login]], expected, post_body=post_body, put_body=put_body)

    def get_empty_category_name_put(self):

        login_username = 'ポムポム'
        user_login = User(pk=1, username=login_username)
        post_body = {'category_name': '実写'}
        put_body= {'category_name': '', 'category_id': MOCK_CATEGORY_UUID_LIST[0]}

        expected: TypeAPIResponse = {
            'body': {
                'message': '登録に失敗しました。',
            },
            'errors': [
                {'fieldName': 'category_name', 'message': 'カテゴリ名を入力してください。'}
            ],
        }

        return self._get_param(login_username, [[user_login]], expected, post_body=post_body, put_body=put_body)


    def get_single_category_delete(self):
        login_username = 'ポムポム'
        user_login = User(pk=1, username=login_username)
        post_body = {'category_name': '実写'}
        delete_body = {'category_id': MOCK_CATEGORY_UUID_LIST[0]}

        expected: TypeAPIResponse = {
            'body': {
                'message': 'ok'
            }
        }

        return self._get_param(login_username, [[user_login]], expected, post_body=post_body, delete_body=delete_body)

    def get_empty_category_id_delete(self):

        login_username = 'ポムポム'
        user_login = User(pk=1, username=login_username)
        post_body = {'category_name': '実写'}
        delete_body= {'category_id': ''}

        expected: TypeAPIResponse = {
            'body': {
                'message': '登録に失敗しました。',
            },
            'errors': [
                {'fieldName': 'category_id', 'message': 'カテゴリIDはUUID形式で指定してください。'}
            ],
        }

        return self._get_param(login_username, [[user_login]], expected, post_body=post_body, delete_body=delete_body)


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