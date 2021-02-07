from django.db.models.base import Model
from app_login.models import User
from typing import List

from django.urls import reverse_lazy

from common.request_response.api_response import SuccessAPIResponse, FailureAPIResponse
from tests.view_utils import ParamViewRequestType, APIResponse, ModelItemsList, Body, get_view_params
from config.messages import messages

MOCK_USER_ID_LIST = [
    'f503f432-7a5a-47e4-bc35-295f0fe2d853',
    '755ce7a0-dafb-46ef-a62f-c1c10e5fafd9',
    '1d16f05b-b3ad-4868-945a-a722de95439f',
]

OK_MESSAGE = messages['common']['success']['response_ok']
LOGIN_FAILURE_MESSAGE = messages['common']['error']['unauthorized']

class DataLoginView:

    def _get_param(self,
        expected: APIResponse,
        model_items_list: ModelItemsList=[],
        post_body: Body={}
    ) -> ParamViewRequestType:

        return get_view_params(
            expected_response=expected, 
            path=reverse_lazy('login:login'),
            model_items_list=model_items_list,
            post_body=post_body
        )

    def get_default_user(self):

        expected: SuccessAPIResponse = {
            'body': {
                'users': [{'username': 'user'}],
                'message': OK_MESSAGE
            }
        }
        return self._get_param(expected, model_items_list=[])

    def get_users(self):
        users = [
            {'username': 'A-pompom1234'},
            {'username': '背景用ユーザ'},
            {'username': 'よく使う　観賞用'},
        ]

        model_users: List[Model] = [
            User(user_id=MOCK_USER_ID_LIST[0], username=users[0]['username']),
            User(user_id=MOCK_USER_ID_LIST[1], username=users[1]['username']),
            User(user_id=MOCK_USER_ID_LIST[2], username=users[2]['username']),
        ]

        expected: SuccessAPIResponse = {
            'body': {
                'users': users,
                'message': OK_MESSAGE
            }
        }
        return self._get_param(expected, model_items_list=[model_users])


    def get_success_login(self):
        users = [
            {'username': 'A-pompom1234'},
        ]
        model_users: List[Model] = [
            User(user_id=MOCK_USER_ID_LIST[0], username=users[0]['username']),
        ]
        post_body = users[0]

        expected: SuccessAPIResponse = {
            'body': {
                'message': OK_MESSAGE
            }
        }
        return self._get_param(expected, model_items_list=[model_users], post_body=post_body)

    def get_failure_login(self):
        post_body = {'username': 'nobody'}

        expected: FailureAPIResponse = {
            'body': {
                'message': LOGIN_FAILURE_MESSAGE
            }
        }
        return self._get_param(expected, post_body=post_body)


data_login_view = DataLoginView()