from rest_framework.exceptions import ErrorDetail
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED, HTTP_422_UNPROCESSABLE_ENTITY
from typing import List, Dict, Any, cast

from rest_framework.utils.serializer_helpers import ReturnDict

from .custom_type import TypeSerializerErrorDict, TypeErrorDict, TypeAPIResponse
from config.messages import messages

class APIResponseHandler:
    """ フロント側で扱いやすいレスポンスへ整形するためのハンドラ """

    def _get_success_response(self, message: str=messages['common']['success']['response_ok'], body: Dict[str, Any]=None) -> TypeAPIResponse:
        """ 処理成功レスポンス 成功メッセージを格納

        Parameters
        ----------
        message : str
            処理成功メッセージ

        Returns
        -------
        TypePostAPIResponse
            PostAPI成功メッセージを格納したレスポンス
        """

        # 単純な登録処理などでは、成功メッセージのみを返却
        if not body:
            return {
                'body': {
                    'message': message
                }
            }
        
        return {
            'body': body
        }

    def render_success(self) -> Response:
        """ 成功メッセージのみ """
        return Response(self._get_success_response(), status=HTTP_200_OK)

    def render_success_body(self, body: Dict[str, Any]) -> Response:
        """ ボディありの成功レスポンスを作成 """
        return Response(self._get_success_response(body=body), status=HTTP_200_OK)

    def render_success_update(self, model_name: str, serializer: Serializer) -> Response:
        """ 更新対象を含むレスポンスを作成

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
            self._get_success_response(
                messages['common']['success']['response_ok'],
                {model_name: serializer.data}
            ),
            status=HTTP_200_OK
        )


    def _get_error_response(self, message: str, errors: TypeSerializerErrorDict) -> TypeAPIResponse:
        """ エラーレスポンスを作成 各フィールドへのエラー内容を格納

        Parameters
        ----------
        message : str
            作成・更新処理失敗メッセージ
        errors : TypeSerializerErrorDict
            フィールド単位でエラーを格納したシリアライザ用エラー辞書

        Returns
        -------
        TypeAPIResponse
            API失敗メッセージと、フィールド単位のエラーメッセージを格納したレスポンス
        """

        # フロントで画面表示しやすい形へ整形
        api_response_errors: List[TypeErrorDict] = [
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

        response = self._get_error_response(
            '登録に失敗しました。',
            cast(TypeSerializerErrorDict, serializor_error)
        )
        return Response(response, status=HTTP_422_UNPROCESSABLE_ENTITY)

    def render_error_by_key(self, error_key: str, error_message: str) -> Response:
        """ キー: 原因で対応するエラーレスポンスを返却

        Parameters
        ----------
        error_key : str
            エラー発生箇所
        error_message : str
            エラー原因メッセージ

        Returns
        -------
        Response
            画面上でユーザへエラーを通知するためのレスポンス
        """

        response = self._get_error_response(
            '登録に失敗しました。',
            {error_key: [ErrorDetail(error_message)]}
        )
        return Response(response, status=HTTP_422_UNPROCESSABLE_ENTITY)


    def render_unauthorized(self) -> Response:
        """ 未ログイン用レスポンスを作成

        Returns
        -------
        Response
            未ログインレスポンス
        """

        response = {
                'body': {
                    'message': messages['common']['error']['unauthorized']
                }
            }
        return Response(data=response, status=HTTP_401_UNAUTHORIZED)

api_response_handler = APIResponseHandler()