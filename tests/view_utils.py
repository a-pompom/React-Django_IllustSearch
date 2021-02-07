from dataclasses import dataclass
from typing import List, Tuple, TypedDict, Optional, Union, Dict, Any

from django.db import models
from rest_framework.test import APIClient
from rest_framework.status import HTTP_401_UNAUTHORIZED

from common.request_response.api_response import SuccessAPIResponse, FailureAPIResponse
from config.messages import messages

# Viewテスト用パラメータ名
VIEW_REQUEST_PARAMS = 'view_request_params'

APIResponse = Union[SuccessAPIResponse, FailureAPIResponse]
ModelItemsList = List[List[models.Model]]
Body = Dict[str, Any]

@dataclass
class ParamViewRequestType:
    """ View機能のテスト用パラメータ """
    expected_response: APIResponse
    path: str
    client: APIClient
    login_username: str
    model_items_list: ModelItemsList
    get_query: str
    post_body: Optional[Body]
    put_body: Optional[Body]
    delete_body: Optional[Body]

def get_view_params(
    expected_response: APIResponse,
    path: str,
    client: APIClient=APIClient(),
    login_username: str='',
    model_items_list: ModelItemsList=[],
    get_query: str='',
    post_body: Optional[Body]=None,
    put_body: Optional[Body]=None,
    delete_body: Optional[Body]=None,
) -> ParamViewRequestType:
    return ParamViewRequestType(expected_response, path, client, login_username, model_items_list, get_query, post_body, put_body, delete_body)


# 共通処理で扱うデータ
class DataCommonViewFunction:

    def get_unauthorized(self) -> Tuple[APIClient, FailureAPIResponse]:

        client = APIClient()
        expected: FailureAPIResponse = {
            'body': {
                'message': messages['common']['error']['unauthorized']
            }
        }

        return (
            client,
            expected
        )

data_common_view_function = DataCommonViewFunction()

TypeCommonFunctionParam = TypedDict("TypeCommonFunctionParam",{
    'login_path': str
})


class TestCommonViewFunction:

    def run_tests(self, params: TypeCommonFunctionParam):
        """ 共通テスト実行処理 各Viewのテストクラスより呼ばれる

        Example
        -------
        test__common(self):
            test_common_view_function.run_tests(...)
        """

        self.unauthorized_for_anonymous_user(params['login_path'])

    def unauthorized_for_anonymous_user(self, login_path: str):

        # GIVEN
        client, expected = data_common_view_function.get_unauthorized()
        # WHEN
        actual = client.get(login_path)
        # THEN
        assert actual.status_code == HTTP_401_UNAUTHORIZED
        assert actual.data == expected

test_common_view_function = TestCommonViewFunction()