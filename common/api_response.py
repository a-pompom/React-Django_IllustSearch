from rest_framework.exceptions import ErrorDetail
from typing import List

from .custom_type import TypeSerializerErrorDict, TypePostErrorDict, TypePostAPIResponse

class APIResponseMixin:
    """ 
    Reactで処理しやすいレスポンスへ整形するためのミックスイン
        シリアライザへ格納されたエラーメッセージをもとに、エラーオブジェクトへ整形
    """

    def render_to_success_response(self, message: str) -> TypePostAPIResponse:
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

        return {
            'message': message
        }

    def render_to_error_response(self, message: str, errors: TypeSerializerErrorDict) -> TypePostAPIResponse:
        """ エラーレスポンスを作成 各フィールドへのエラー内容を格納

        Parameters
        ----------
        message : str
            POST処理失敗メッセージ
        errors : TypeSerializerErrorDict
            フィールド単位でエラーを格納したシリアライザ用エラー辞書

        Returns
        -------
        TypePostAPIResponse
            PostAPI失敗メッセージと、フィールド単位のエラーメッセージを格納したレスポンス
        """

        api_response_errors: List[TypePostErrorDict] = []

        # Reactで画面表示しやすい形へ整形
        for field_name, error_details in errors.items():
            api_response_errors.append(
                {
                    'fieldName': field_name,
                    'message': self.get_error_message(error_details),
                }
            )

        return {
            'message': message,
            'errors': api_response_errors,
        }

    def get_error_message(self, errors: List[ErrorDetail]) -> str:
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

        # 単一要素から成る場合は結合は不要
        if len(errors) == 1:
            return errors[0]

        error_message = ','.join([error for error in errors])

        return error_message
