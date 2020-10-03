from typing import Union, cast

from django.contrib.auth.models import AbstractBaseUser, AnonymousUser
from django.http.response import HttpResponse
from django.views.generic.base import View
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_401_UNAUTHORIZED

from .api_response import use_api_response
from app_login.models import User

from .custom_type import TypeLoginUserHandler

UnknownUser = Union[User, AnonymousUser]

def use_login_user_handler() -> TypeLoginUserHandler:

    mixin = LoginUserHandlerMixin()

    return {
        'get_login_user_id': mixin.get_login_user_id
    }

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
        if not cast(AbstractBaseUser, request.user).is_authenticated:
            return None

        user = cast(User, request.user)
        return user.get_id()

    def dispatch(self, request: Request, *args, **kwargs) -> HttpResponse:
        """ 各Viewメソッドの前処理として、ログイン済みか判定

        Parameters
        ----------
        request : Request
            ログインユーザもしくは匿名ユーザを格納したリクエスト

        Returns
        -------
        HttpResponse
            未ログイン -> 401 unauthorized
            ログイン済 -> Viewから返されるHttpResponse
        """

        api_response_handler = use_api_response()

        if not self.get_login_user_id(request):
            return Response(api_response_handler['render_to_failure_response'](''), status=HTTP_401_UNAUTHORIZED)

        return cast(View, super()).dispatch(request, *args, **kwargs)