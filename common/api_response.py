from rest_framework.exceptions import ErrorDetail
from typing import List, Dict, Any

from .custom_type import TypeSerializerErrorDict, TypeErrorDict, TypeAPIResponse

class APIResponseHandler:
    """ 
    Reactで処理しやすいレスポンスへ整形するためのミックスイン
        シリアライザへ格納されたエラーメッセージをもとに、エラーオブジェクトへ整形
    """

    def render_to_success_response(self, message: str='ok', body: Dict[str, Any]=None) -> TypeAPIResponse:
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

    def render_to_error_response(self, message: str, errors: TypeSerializerErrorDict) -> TypeAPIResponse:
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

        # Reactで画面表示しやすい形へ整形
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

    def render_to_failure_response(self, message: str) -> TypeAPIResponse:
        """ ログイン失敗など、シリアライザに関係しないエラーレスポンスを生成

        Parameters
        ----------
        message : str
            エラーメッセージ

        Returns
        -------
        TypeAPIResponse
            エラ〜メッセージを格納したAPIResponse
        """

        return {
                'body': {
                    'message': message
                }
            }

api_response_handler = APIResponseHandler()