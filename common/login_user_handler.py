from typing import Union, cast

from django.contrib.auth.models import AnonymousUser
from rest_framework import views
from rest_framework.request import Request

from app_login.models import User
from common.exception_handler import UnAuthorizedException

class LoginUserHandler:
    """ ログインユーザに関連する処理を扱うためのハンドラ"""

    def get_login_user_id(self, request: Request) -> Union[None, int]:
        """ ログインユーザの識別子を取得

        Parameters
        ----------
        request : Request
            セッションから復元したユーザ情報を持つリクエスト

        Returns
        -------
        user_id : Union[None, int]
            未ログイン -> None
            ログイン済 -> ユーザ識別子
        """

        # 未ログイン
        if isinstance(request.user, AnonymousUser) and not request.user.is_authenticated:
            return None

        user = cast(User, request.user)
        return user.get_id()


class LoginRequiredMixin:
    """ ログイン確認のための前処理を実行するためのミックスイン """

    def initial(self, request: Request, *args, **kwargs):
        """ ログイン済か判定

        Parameters
        ----------
        request : Request
            送信されたrequestオブジェクト

        Raises
        ------
        UnAuthorizedException
            未ログイン時に送出される
        """

        # 未ログイン
        # APIViewからEXCEPTION_HANDLERが呼ばれる
        if login_user_handler.get_login_user_id(request) is None:
            raise UnAuthorizedException()

        # APIViewのinitialメソッドでリクエストを処理
        cast(views.APIView, super()).initial(request, *args, **kwargs)


login_user_handler = LoginUserHandler()