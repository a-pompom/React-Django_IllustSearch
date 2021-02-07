from django.contrib.auth.backends import BaseBackend
from rest_framework.request import Request
from typing import Any, Optional, Union

from common.exception.app_exception import LoginFailureException
from .models import User

class AuthBackend(BaseBackend):
    """ 認証処理用バックエンド
    """

    def get_user(self, user_id: str) -> Union[User, None]:
        """ セッションに格納されているユーザ識別用キーをもとにユーザモデルを取得
        Parameters
        ----------
        user_id: str
            一意識別子
        
        Returns
        -------
        user: User
            認証用ユーザ
        """

        try:
            user = User.objects.get(user_id=user_id)

        except (User.DoesNotExist, ValueError):
            return None
        
        return user

    def authenticate(self, request: Request, username: Optional[str]=None, password: Optional[str]=None, **kwargs: Any) -> User:
        """ 認証処理 ユーザ名・パスワードをもとに、該当するユーザがDBに存在するか検証
        Parameters
        ----------
        request: HttpRequest
            認証で利用されるリクエスト情報
        username: str
            ユーザをDBから取得するためのユーザ名
        password: str
            ユーザを認証するためのパスワード 今回はローカルでのみ使うことを想定しているので、未使用
        
        Returns
        -------
        user: User
            認証に成功した場合は、セッションへ格納するためのユーザモデルを返す
        Raises
        ------
        LoginFailureException
            ログインに失敗した場合に送出される
        """

        # ユーザ存在チェック
        try:
            user = User.objects.get(username=username)

        except User.DoesNotExist:
            raise LoginFailureException()

        return user