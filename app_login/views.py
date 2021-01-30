from typing import Callable

from django.contrib.auth import login
from django.db.models.base import Model
from rest_framework import views
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from .backend import AuthBackend
from .models import User
from .serializer import LoginSerializer, SignupSerializer

from common.exception.app_exception import LoginFailureException
from common.model.validator import is_unique_model
from common.request_response.single_model_view_handler import get_single_model_view_handler
from common.request_response.api_response import api_response_handler
from common.request_response.login_user_handler import LoginRequiredMixin


class LoginView(views.APIView):
    """ ログインAPI用View """

    def get(self, request: Request) -> Response:
        """ ログイン画面表示 ユーザの一覧もあわせて取得

        Parameters
        ----------
        request : Request
            リクエスト情報 未使用

        Returns
        -------
        Response
            ユーザ情報JSONを格納したレスポンス
        """

        user = User.objects.all()

        # ユーザが空のときは、デフォルトユーザとしてルートユーザを作成
        if not len(user):
            root_user = User(
                username='user',
            )
            root_user.save()
            user = User.objects.all()

        serializer = LoginSerializer(instance=user, many=True)

        return api_response_handler.success.render_with_body({'body': {'users': serializer.data}})

    def post(self, request: Request) -> Response:
        """ ログイン処理 ログインの成否はステータスコードで判定

        Parameters
        ----------
        request : Request
            ユーザ名を格納したリクエスト

        Returns
        -------
        Response
            ログイン成功-> ステータス200
            ログイン失敗-> ステータス401

        Raises
        ------
        LoginFailureException
            ユーザ名が誤っていた場合、送出される ログイン失敗として判定するために利用
        """

        serializer = LoginSerializer(data=request.data)

        try:
            if not serializer.is_valid(raise_exception=False):
                raise LoginFailureException()
            
            user = AuthBackend().authenticate(
                request, 
                username=serializer.validated_data['username'], 
            )

        # ログイン失敗
        except LoginFailureException as ex:

            return api_response_handler.failure.render_unauthorized()

        # 認証処理で得られたユーザでセッションを発行
        login(request, user, 'app_login.backend.AuthBackend')

        # ログイン成功
        return api_response_handler.success.render()


class SignUpView(views.APIView):
    """ ユーザ登録API用View """

    def __init__(self):
        self._single_model_view_handler = get_single_model_view_handler('signup', SignupSerializer, User)

    def post(self, request: Request) -> Response:
        """ ユーザ登録処理
        Parameters
        ----------
        request : HttpRequest
            POSTリクエスト情報
        Returns
        -------
        Response
            ユーザ登録失敗 -> エラーメッセージを格納したレスポンス
            ユーザ登録成功 -> 登録成功メッセージ
        """        

        get_model_instance: Callable[[Serializer], Model] = lambda serializer: User(username=serializer.validated_data['username'])

        return self._single_model_view_handler.post(
            SignupSerializer(data=request.data),
            get_model_instance
        )


class UserValidateUniqueView(views.APIView):
    """ ユーザがユニークかフロントからのリクエストで検証するためのView """

    def post(self, request: Request) -> Response:
        """ ユーザがユニークか検証

        Parameters
        ----------
        request : Request
            検証対象ユーザ名を格納したリクエスト

        Returns
        -------
        Response
            ユニーク-> OKレスポンス ユニークでない-> ユーザ名フィールドへエラーメッセージを詰め込んだレスポンス
        """

        username = request.data['username']

        # ユニーク
        if is_unique_model(User, {'username': username}):
            return api_response_handler.success.render()

        # ユニークでない
        return api_response_handler.failure.render_field_error({'username': ['ユーザ名は既に使用されています。']})


class AuthenticationView(LoginRequiredMixin, views.APIView):
    """ ログインが必要な画面で前処理として呼ばれる認証用APIView """

    def get(self, request: Request) -> Response:
        """ 認証済みか判定 未認証の場合は、ミックスインにより、401レスポンスが返される

        Parameters
        ----------
        request : Request
            Request

        Returns
        -------
        Response
            ログイン済み-> 200, 未ログイン-> 401
        """

        return api_response_handler.success.render()