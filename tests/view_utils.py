from typing import List, Tuple, TypedDict, Optional

from rest_framework.test import APIClient
from rest_framework.status import HTTP_401_UNAUTHORIZED

from common.custom_type import TypeAPIResponse
from config.messages import messages

# 共通処理で扱うデータ
class DataCommonViewFunction:

    def get_unauthorized(self) -> Tuple[APIClient, TypeAPIResponse]:

        client = APIClient()
        expected: TypeAPIResponse = {
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