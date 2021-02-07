from typing import Dict, Tuple, List, Optional, Any, Union, cast
from uuid import UUID

from django.urls import reverse_lazy
from django.db import models

from app_illust_list.models import Category
from app_login.models import User

from common.request_response.api_response import FailureAPIResponse, SuccessAPIResponse
from tests.view_utils import ParamViewRequestType, get_view_params

MOCK_USER_ID_LIST = [
    'a4c0158c-3cc0-4f40-9519-5f123b2ab799',
    '9ebff94e-a3df-4782-afca-fd62df59a408',
    'c5cd4d37-bf0d-4a59-9707-ef8a75dd1912',
]

MOCK_CATEGORY_UUID_LIST = [
    'f503f432-7a5a-47e4-bc35-295f0fe2d853',
    '755ce7a0-dafb-46ef-a62f-c1c10e5fafd9',
    '1d16f05b-b3ad-4868-945a-a722de95439f',
    '42ca47c3-369b-4dd2-87ff-618f3d67cea0',
]

def get_path() -> str:
    return reverse_lazy('illust_list:category')

def get_param(
    expected: Union[SuccessAPIResponse, FailureAPIResponse],
    login_username: str='', 
    model_items_list: List[List[models.Model]]=[],
    post_body: Dict[str, Any] = {},
    put_body: Dict[str, Any] = {},
    delete_body: Dict[str, Any] = {},
) -> ParamViewRequestType:

    return get_view_params(
        expected, 
        path=get_path(),
        login_username=login_username,
        model_items_list=model_items_list,
        post_body=post_body,
        put_body=put_body,
        delete_body=delete_body
    )


class DataGet:

    def get_success_get(self) -> ParamViewRequestType:

        login_username = 'ポムポム'

        # Users
        user_login = User(user_id=MOCK_USER_ID_LIST[0], username=login_username)
        user_not_login = User(user_id=MOCK_USER_ID_LIST[1], username='purin')

        # Category
        category_list = [
            Category(category_id=MOCK_CATEGORY_UUID_LIST[0], user_id=user_login, category_name='写真', sort_order=1),
            Category(category_id=MOCK_CATEGORY_UUID_LIST[1], user_id=user_login, category_name='イラスト', sort_order=2),
            Category(category_id=MOCK_CATEGORY_UUID_LIST[2], user_id=user_not_login, category_name='イラスト', sort_order=1),
            Category(category_id=MOCK_CATEGORY_UUID_LIST[3], user_id=user_not_login, category_name='背景', sort_order=2),
        ]
        desc_order_category_list = [category_list[0], category_list[1]]

        expected: SuccessAPIResponse = {
            'body': {
                'category_list': [
                    {
                        'category_id': category.category_id, 
                        'category_name': category.category_name, 
                        'user_id': UUID(category.user_id.user_id), 
                        'sort_order': category.sort_order
                    } for category in desc_order_category_list],
                'message': 'ok'
            }
        }

        return get_param(expected, login_username, model_items_list=[[user_login, user_not_login], [category_list[0], category_list[1], category_list[2], category_list[2]]])


class DataPost:

    def get_single_category(self):
        login_username = 'ポムポム'
        user_login = User(user_id=MOCK_USER_ID_LIST[0], username=login_username)
        post_body = {'category_name': '実写'}

        expected: SuccessAPIResponse = {
            'body': {
                'category': {'category_id': '', 'category_name': '実写', 'user_id': UUID(MOCK_USER_ID_LIST[0]), 'sort_order': 1},
                'message': 'ok'
            }
        }

        return get_param(expected, login_username, model_items_list=[[user_login]], post_body=post_body)


    def get_empty_category_post(self):
        login_username = 'ポムポム'
        user_login = User(user_id=MOCK_USER_ID_LIST[0], username=login_username)
        post_body = {'category_name': ''}

        expected: FailureAPIResponse = {
            'body': {
                'message': '登録に失敗しました。',
            },
            'errors': [
                {'fieldName': 'category_name', 'message': 'カテゴリ名を入力してください。'}
            ],
        }

        return get_param(expected, login_username, model_items_list=[[user_login]], post_body=post_body)

    def get_duplicate_category_post(self):
        login_username = 'ポムポム'
        user_login = User(user_id=MOCK_USER_ID_LIST[0], username=login_username)
        post_body = {'category_name': '実写'}

        expected: FailureAPIResponse = {
            'body': {
                'message': '登録に失敗しました。',
            },
            'errors': [
                {'fieldName': 'category_name', 'message': 'カテゴリ名は既に使用されています。'}
            ],
        }

        return get_param(expected, login_username, model_items_list=[[user_login]], post_body=post_body)


class DataPut:

    def get_single_category_put(self):
        login_username = 'ポムポム'
        user_login = User(user_id=MOCK_USER_ID_LIST[0], username=login_username)
        category = Category(category_id=MOCK_CATEGORY_UUID_LIST[0],category_name='実写', user_id=user_login, sort_order=1)
        put_body = {'category_name': '実写画像', 'category_id': MOCK_CATEGORY_UUID_LIST[0]}

        expected: FailureAPIResponse = {
            'body': {
                'category': {'category_id': MOCK_CATEGORY_UUID_LIST[0], 'category_name': '実写画像', 'user_id': UUID(MOCK_USER_ID_LIST[0]), 'sort_order': 1},
                'message': 'ok'
            }
        }

        return get_param(expected, login_username, model_items_list=[[user_login], [category]], put_body=put_body)

    def get_empty_category_id_put(self):

        login_username = 'ポムポム'
        user_login = User(user_id=MOCK_USER_ID_LIST[0], username=login_username)
        category = Category(category_id=MOCK_CATEGORY_UUID_LIST[0],category_name='実写', user_id=user_login)
        put_body= {'category_name': '実写映画', 'category_id': ''}

        expected: FailureAPIResponse = {
            'body': {
                'message': '登録に失敗しました。',
            },
            'errors': [
                {'fieldName': 'category_id', 'message': 'カテゴリIDはUUID形式で指定してください。'}
            ],
        }

        return get_param(expected, login_username, model_items_list=[[user_login], [category]], put_body=put_body)

    def get_empty_category_name_put(self):

        login_username = 'ポムポム'
        user_login = User(user_id=MOCK_USER_ID_LIST[0], username=login_username)
        category = Category(category_id=MOCK_CATEGORY_UUID_LIST[0],category_name='実写', user_id=user_login)
        put_body= {'category_name': '', 'category_id': MOCK_CATEGORY_UUID_LIST[0]}

        expected: FailureAPIResponse = {
            'body': {
                'message': '登録に失敗しました。',
            },
            'errors': [
                {'fieldName': 'category_name', 'message': 'カテゴリ名を入力してください。'}
            ],
        }

        return get_param(expected, login_username, model_items_list=[[user_login], [category]], put_body=put_body)


class DataDelete:

    def get_single_category_delete(self):
        login_username = 'ポムポム'
        user_login = User(user_id=MOCK_USER_ID_LIST[0], username=login_username)
        category = Category(category_id=MOCK_CATEGORY_UUID_LIST[0],category_name='実写', user_id=user_login)
        delete_body = {'category_id': MOCK_CATEGORY_UUID_LIST[0]}

        expected: SuccessAPIResponse = {
            'body': {
                'message': 'ok'
            }
        }

        return get_param(expected, login_username, model_items_list=[[user_login], [category]], delete_body=delete_body)

    def get_empty_category_id_delete(self):

        login_username = 'ポムポム'
        user_login = User(user_id=MOCK_USER_ID_LIST[0], username=login_username)
        delete_body= {'category_id': ''}

        expected: FailureAPIResponse = {
            'body': {
                'message': '登録に失敗しました。',
            },
            'errors': [
                {'fieldName': 'category_id', 'message': 'カテゴリIDはUUID形式で指定してください。'}
            ],
        }

        return get_param(expected, login_username, model_items_list=[[user_login]], delete_body=delete_body)


data_get = DataGet()
data_post = DataPost()
data_put = DataPut()
data_delete = DataDelete()