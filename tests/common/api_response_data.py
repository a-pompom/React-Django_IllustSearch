from typing import Tuple, Optional, Any
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED, HTTP_422_UNPROCESSABLE_ENTITY

from app_login.models import User
from app_login.serializer import SignupSerializer
from config.messages import messages

from common.api_response import SuccessAPIResponse, FailureAPIResponse, FieldError

# メッセージ, ボディ, 期待結果
SuccessParamType = Tuple[str, Any, Response]
# モデル名, モデルインスタンスを格納したシリアライザ
SuccessUpdateParamType = Tuple[str, Serializer, Response]

FieldErrorParamType = Tuple[Response, FieldError]
ErrorParamType = Response


OK_MESSAGE = messages['common']['success']['response_ok']

class DataSuccess:

    def _get_params(self, expected: Response, message=OK_MESSAGE, body=None) -> SuccessParamType:
        return (
            message,
            body,
            expected,
        )

    def get_render(self) -> SuccessParamType:
        expected_response: SuccessAPIResponse = {
            'body': {
                'message': OK_MESSAGE
            }
        }
        expected = Response(data=expected_response, status=HTTP_200_OK)
        return self._get_params(expected)

    def get_render_with_body(self) -> SuccessParamType:
        body = {
            'message': OK_MESSAGE,
            'user': {
                'name': 'pompom',
                'age': 20,
            }
        }

        expected_response: SuccessAPIResponse = {
            'body': body
        }
        expected = Response(data=expected_response, status=HTTP_200_OK)
        return self._get_params(expected, body=body)


class DataSuccessUpdateModel:

    def _get_params(self, expected: Response, model_name: str, serializer: Serializer) -> SuccessUpdateParamType:
        return (
            model_name,
            serializer,
            expected,
        )

    def get_render_with_updated_model(self) -> SuccessUpdateParamType:

        model_name = 'user'
        model_object = User(username='pompom')
        serializer = SignupSerializer(instance=model_object)

        expected_response: SuccessAPIResponse = {
            'body': {
                'message': OK_MESSAGE,
                'user': {
                    'username': 'pompom'
                }
            }
        }
        expected = Response(data=expected_response, status=HTTP_200_OK)

        return self._get_params(expected, model_name, serializer)

class DataFailure:

    def _get_params(self, expected: Response) -> ErrorParamType:
        return expected

    def get_unauthorized_error(self):

        expected_response: FailureAPIResponse = {
            'body': {
                'message': messages['common']['error']['unauthorized']
            }
        }
        expected = Response(data=expected_response, status=HTTP_401_UNAUTHORIZED)

        return self._get_params(expected)


class DataFieldError:

    def _get_params(self, expected: Response, field_error: FieldError) -> FieldErrorParamType:

        return (
            expected,
            field_error
        )

    def get_single_field_error(self):

        field_name = 'username'
        error_messages = ['ユーザ名を入力してください。']
        errors: FieldError = {field_name: error_messages}

        expected_response: FailureAPIResponse = {
            'body': {
                'message': messages['common']['error']['update_failure']
            },
            'errors': [{
                'fieldName': field_name,
                'message': error_messages[0]
            }]
        }

        expected = Response(data=expected_response, status=HTTP_422_UNPROCESSABLE_ENTITY)

        return self._get_params(expected, field_error=errors)

    def get_comma_separated_field_error(self) -> FieldErrorParamType:
        field_name = 'age'
        error_messages = ['数値を入力してください。', '年齢は0以上の整数を入力してください。']
        errors: FieldError = {
            field_name: error_messages
        }

        expected_response: FailureAPIResponse = {
            'body': {
                'message': messages['common']['error']['update_failure']
            },
            'errors': [{
                'fieldName': field_name,
                'message': ', '.join(error_messages)
            }]
        }
        expected = Response(data=expected_response, status=HTTP_422_UNPROCESSABLE_ENTITY)

        return self._get_params(expected, field_error=errors)

    def get_multiple_field_error(self) -> FieldErrorParamType:

        field_name_list = ['password', 'confirmPassword']
        error_messages = [
            ['半角英数で入力してください。', '10文字以上で入力してください。'],
            ['パスワードが一致しません。']
        ]
        field_error: FieldError = {
            field_name_list[0]: error_messages[0],
            field_name_list[1]: error_messages[1],
        }

        expected_response: FailureAPIResponse = {
            'body': {
                'message': messages['common']['error']['update_failure']
            },
            'errors': [
                {
                    'fieldName': field_name_list[0],
                    'message': ', '.join(error_messages[0])
                },
                {
                    'fieldName': field_name_list[1],
                    'message': ', '.join(error_messages[1])
                },
            ]
        }
        expected = Response(data=expected_response, status=HTTP_422_UNPROCESSABLE_ENTITY)

        return self._get_params(expected, field_error=field_error)


data_success = DataSuccess()
data_success_update = DataSuccessUpdateModel()
data_failure = DataFailure()
data_field_error = DataFieldError()