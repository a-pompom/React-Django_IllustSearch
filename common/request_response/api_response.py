from rest_framework.exceptions import ErrorDetail
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED, HTTP_422_UNPROCESSABLE_ENTITY
from rest_framework.utils.serializer_helpers import ReturnDict
from typing import List, Dict, Any, cast, TypedDict, Optional

from config.messages import messages

Body = Dict[str, Any]
# フィールドごとに格納されたエラーオブジェクト
FieldError = Dict[str, List[str]]
FieldErrorDetail = Dict[str, List[ErrorDetail]]

class FieldErrorResponse(TypedDict):
    """ エラーオブジェクト """
    fieldName: str
    message: str

class SuccessAPIResponse(TypedDict):
    """ 成功APIレスポンス """

    body: Body

class FailureAPIResponse(TypedDict, total=False):
    """ 失敗APIレスポンス """

    body: Body
    errors: Optional[List[FieldErrorResponse]]


class _SuccessHandler:
    """ 処理成功時に受け取るレスポンスを生成 """
    def _get_response(self, message: str=messages['common']['success']['response_ok'], body: Dict[str, Any]=None) -> SuccessAPIResponse:
        """ 処理成功レスポンス 成功メッセージを格納

        Parameters
        ----------
        message : str
            処理成功メッセージ

        Returns
        -------
        SuccessAPIResponse
            API成功メッセージを格納したレスポンス
        """

        # 単純な登録処理などでは、成功メッセージのみを返却
        if not body:
            return {
                'body': {
                    'message': message
                }
            }

        body['message'] = message
        return {
            'body': body
        }

    def render(self) -> Response:
        """ 成功メッセージのみ """
        return Response(self._get_response(), status=HTTP_200_OK)

    def render_with_body(self, body: Body) -> Response:
        """ ボディありの成功レスポンスを作成 """
        return Response(self._get_response(body=body), status=HTTP_200_OK)

    def render_with_updated_model(self, model_name: str, serializer: Serializer) -> Response:
        """ 更新対象モデルを含むレスポンスを作成

        Parameters
        ----------
        model_name : str
            更新対象オブジェクト名
        serializer : Serializer
            Modelのインスタンスをもとに生成されたシリアライザ

        Returns
        -------
        Response
            更新対象を格納したレスポンス
        """
        
        return Response(
            self._get_response(
                body={model_name: serializer.data}
            ),
            status=HTTP_200_OK
        )


class _FailureHandler:
    """ 失敗時に受け取るレスポンスを生成 """
    def _get_response(self, message: str, errors: FieldErrorDetail) -> FailureAPIResponse:
        """ エラーレスポンスを作成 各フィールドへのエラー内容を格納

        Parameters
        ----------
        message : str
            作成・更新処理失敗メッセージ
        errors : FieldErrorDetail
            フィールド単位でエラーを格納したシリアライザ用エラー辞書

        Returns
        -------
        FailureAPIResponse
            API失敗メッセージと、フィールド単位のエラーメッセージを格納したレスポンス
        """

        # フロントで画面表示しやすい形へ整形
        api_response_errors: List[FieldErrorResponse] = [
            {
                'fieldName': field_name,
                'message': self._get_error_message(error_details)
            } for field_name, error_details in errors.items()
        ]

        return {
            'body': {
                'message': message
            },
            'errors': api_response_errors,
        }

    def _get_error_message(self, errors: List[ErrorDetail]) -> str:
        """ ErrorDetailをもとにフィールドへ表示するエラーメッセージ文字列を作成

        Parameters
        ----------
        errors : List[ErrorDetail]
            フィールドへ設定されたエラーメッセージの一覧

        Returns
        -------
        str
            各エラーメッセージをカンマ区切りで結合したエラーメッセージ文字列
        """

        error_message = ', '.join([error for error in errors])

        return error_message

    def render_validation_error(self, serializor_error: ReturnDict) -> Response:
        """ バリデーションエラー用レスポンスを作成

        Parameters
        ----------
        serializor_error : ReturnDict
            シリアライザの持つエラー属性

        Returns
        -------
        Response
            バリデーションエラー内容を含むレスポンス
        """

        response = self._get_response(
            messages['common']['error']['update_failure'],
            cast(FieldErrorDetail, serializor_error)
        )
        return Response(response, status=HTTP_422_UNPROCESSABLE_ENTITY)

    def render_field_error(self, field_error: FieldError) -> Response:
        """ 画面上のフィールドに対応するエラーレスポンスを作成

        Parameters
        ----------
        field_error: FieldError
            フィールド名: エラーメッセージリスト形式でエラー情報を格納した辞書\n
            ex) {"username": ["8文字以上で入力", "半角英数のみ"], "confirm_passsword": ["パスワード不一致"]}

        Returns
        -------
        Response
            画面上でユーザへエラーを通知するためのレスポンス
        """

        error_detail: FieldErrorDetail = {}
        for field in field_error.keys():
            error_detail[field] = [ErrorDetail(error_message) for error_message in field_error[field]]

        response = self._get_response(
            messages['common']['error']['update_failure'],
            error_detail
        )
        return Response(response, status=HTTP_422_UNPROCESSABLE_ENTITY)


    def render_unauthorized(self) -> Response:
        """ 未ログイン用レスポンスを作成

        Returns
        -------
        Response
            未ログインレスポンス
        """

        response: FailureAPIResponse = {
                'body': {
                    'message': messages['common']['error']['unauthorized']
                }
            }
        return Response(data=response, status=HTTP_401_UNAUTHORIZED)


class _APIResponseHandler:
    """ フロント側で扱いやすいレスポンスへ整形するためのハンドラ """

    def __init__(self):
        self.success = _SuccessHandler()
        self.failure = _FailureHandler()


api_response_handler = _APIResponseHandler()