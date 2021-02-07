from app_login.models import User

from django.urls import reverse_lazy

from app_login.serializer import USERNAME_MAX_LENGTH
from common.request_response.api_response import SuccessAPIResponse, FailureAPIResponse
from tests.view_utils import ParamViewRequestType, APIResponse, ModelItemsList, Body, get_view_params
from config.messages import messages

class DataSignupView:

    def _get_param(self,
        expected: APIResponse,
        model_items_list: ModelItemsList=[],
        post_body: Body={},
    ) -> ParamViewRequestType:
        return get_view_params(
            expected_response=expected,
            path=reverse_lazy('login:signup'),
            model_items_list=model_items_list,
            post_body=post_body
        )

    def get_success_post(self) -> ParamViewRequestType:

        post_body = {'username': 'A-pompom1234'}

        expected: SuccessAPIResponse = {
            'body': {
                'message': 'ok',
                'user': {'username': 'A-pompom1234'}
            }
        }

        return self._get_param(expected, post_body=post_body)

    def get_too_long_username(self) -> ParamViewRequestType:
        username = '01234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789'
        post_body = {'username': username}

        expected: FailureAPIResponse = {
            'body': {
                'message': messages['common']['error']['update_failure']
            },
            'errors': [
                {
                    'fieldName': 'username',
                    'message': f'ユーザ名は{USERNAME_MAX_LENGTH}文字以下で入力してください。',
                }
            ]
        }
        
        return self._get_param(expected, post_body=post_body)

    def get_user_duplicate(self) -> ParamViewRequestType:

        username = 'A-pompom1234'
        post_body = {'username': username}

        duplicate_user = User(username=username)

        expected: FailureAPIResponse = {
            'body': {
                'message': messages['common']['error']['update_failure']
            },
            'errors': [
                {
                    'fieldName': 'username',
                    'message': 'ユーザ名はすでに使用されています。',
                }
            ]
        }

        return self._get_param(expected, model_items_list=[[duplicate_user]], post_body=post_body)


data_signup_view = DataSignupView()