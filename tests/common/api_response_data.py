from typing import Tuple

from common.custom_type import *

class DataRenderToSuccessResponse:

    # メッセージ, ボディ, 期待結果
    ParamType = Tuple[str, Any, TypeAPIResponse]
    message = 'ok'

    def _get_params(self, body=None) -> ParamType:
        if body is None:
            return (
                self.message,
                None,
                {
                    'body': {
                        'message': self.message
                    }
                },
            )

        body['message'] = self.message

        return (
            self.message,
            body,
            {
                'body': body
            },
        )

    def get_only_message(self) -> ParamType:
        return self._get_params()

    def get_response_with_body(self) -> ParamType:
        return self._get_params({
            'users': ['pompom', 'a-pompom', 'ユーザ']
        })


class DataRenderToErrorResponse:

    # メッセージ, 整形用エラーオブジェクト, 期待結果
    ParamType = Tuple[str, TypeSerializerErrorDict, TypeAPIResponse]
    message = '入力内容に誤りがあります。'

    def get_params(self, errors: TypeSerializerErrorDict, expected_errors: List[TypeErrorDict]) -> ParamType:
        return (
            self.message,
            errors,
            {
                'body': {
                    'message': self.message
                },
                'errors': expected_errors
            }
        )

    def get_single_field_error(self) -> ParamType:

        field_name = 'username'
        error_message = 'ユーザ名を入力してください。'
        errors: TypeSerializerErrorDict = {
            field_name: [ErrorDetail(error_message)]
        }

        expected_errors: List[TypeErrorDict] = [
            {
                'fieldName': field_name,
                'message': error_message
            }
        ]

        return self.get_params(errors, expected_errors)

    def get_comma_separated_field_error(self) -> ParamType:

        field_name = 'age'
        error_messages = ['数値を入力してください。', '年齢は0以上の整数を入力してください。']
        errors: TypeSerializerErrorDict = {
            field_name: [ErrorDetail(error_messages[0]), ErrorDetail(error_messages[1])]
        }

        expected_errors: List[TypeErrorDict] = [
            {
                'fieldName': field_name,
                'message': ', '.join(error_messages)
            }
        ]

        return self.get_params(errors, expected_errors)

    def get_multiple_field_error(self) -> ParamType:

        field_name_list = ['password', 'confirmPassword']
        error_messages = [
            ['半角英数で入力してください。', '10文字以上で入力してください。'],
            ['パスワードが一致しません。']
        ]
        errors: TypeSerializerErrorDict = {
            field_name_list[0]: [ErrorDetail(error_messages[0][0]), ErrorDetail(error_messages[0][1])],
            field_name_list[1]: [ErrorDetail(error_messages[1][0])]
        }

        expected_errors: List[TypeErrorDict] = [
            {
                'fieldName': field_name_list[0],
                'message': ', '.join(error_messages[0])
            },
            {
                'fieldName': field_name_list[1],
                'message': ', '.join(error_messages[1])
            },
        ]

        return self.get_params(errors, expected_errors)


class DataRenderToFailureResponse:

    # メッセージ, 期待結果
    ParamType = Tuple[str, TypeAPIResponse]
    message = 'ログインしてください。'

    def _get_param(self) -> ParamType:
        return (
            self.message,
            {
                'body': {
                    'message': self.message
                }
            }
        )

    def get_failure(self):
        return self._get_param()

data_render_success_response = DataRenderToSuccessResponse()
data_render_to_error_response = DataRenderToErrorResponse()
data_render_to_failure_response = DataRenderToFailureResponse()