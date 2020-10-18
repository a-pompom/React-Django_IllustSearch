from typing import TypedDict, Union, cast
from typing_extensions import Protocol

from django.contrib.auth.models import AnonymousUser
from rest_framework import views
from rest_framework.request import Request

from app_login.models import User
from common.exception_handler import UnAuthorizedException

class LoginUserHandlerMixin():
    """ ログインユーザ情報を扱うためのミックスイン
    """

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
        if self.get_login_user_id(request) is None:
            raise UnAuthorizedException()

        # APIViewのinitialメソッドでリクエストを処理
        cast(views.APIView, super()).initial(request, *args, **kwargs)


class GetLoginUserId(Protocol):
    def __call__(self, request: Request) -> Union[None, int]: ...

class TypeUseLoginUserHandler(TypedDict):
    """ログインユーザハンドラを扱うための関数群 """
    get_login_user_id: GetLoginUserId

def use_login_user_handler() -> TypeUseLoginUserHandler:
    """ ログインユーザハンドラミックスインを関数形式で取得

    Returns
    -------
    TypeUseLoginUserHandler
        ログインユーザハンドラミックスインのメソッドを格納したディクショナリ
    """

    mixin = LoginUserHandlerMixin()

    return {
        'get_login_user_id': mixin.get_login_user_id
    }
