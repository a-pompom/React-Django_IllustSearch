from rest_framework.exceptions import ErrorDetail
from common.custom_type import TypeSerializerErrorDict
from django.contrib.auth import login
from typing import cast

from rest_framework import status, views
from rest_framework.request import Request
from rest_framework.response import Response

from .backend import AuthBackend
from .exception import LoginFailureException
from .models import User
from .serializer import LoginSerializer, SignupSerializer

from common import custom_type
from common.validator import is_unique_model
from common.api_response import api_response_handler
from common.login_user_handler import LoginRequiredMixin


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

        response = api_response_handler.render_to_success_response('ok', {'users': serializer.data})
        return Response(response, status=status.HTTP_200_OK)

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

            return Response(api_response_handler.render_to_error_response('ログインに失敗しました。', ex.errors), status=status.HTTP_401_UNAUTHORIZED)

        # 認証処理で得られたユーザでセッションを発行
        login(request, user, 'app_login.backend.AuthBackend')

        # ログイン成功
        return Response(api_response_handler.render_to_success_response('ログイン成功。'), status=status.HTTP_200_OK)

class SignUpView(views.APIView):
    """ ユーザ登録API用View """

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

        serializer = SignupSerializer(data=request.data)

        # 登録失敗
        if not serializer.is_valid():
            response = api_response_handler.render_to_error_response('登録に失敗しました。', cast(custom_type.TypeSerializerErrorDict, serializer.errors))

            return Response(response, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        # ユーザ登録
        user = User(
            username=serializer.validated_data['username'],
        )
        user.save()

        # 登録成功
        response = api_response_handler.render_to_success_response('登録しました。')
        return Response(response, status=status.HTTP_200_OK)

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
            return Response(api_response_handler.render_to_success_response('OK'), status=status.HTTP_200_OK)

        # ユニークでない
        error_response: TypeSerializerErrorDict = {
            'username': [ErrorDetail('ユーザ名は既に使用されています。')]
        }

        return Response(api_response_handler.render_to_error_response('error', error_response), status=status.HTTP_422_UNPROCESSABLE_ENTITY)

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

        return Response(api_response_handler.render_to_success_response('OK'), status=status.HTTP_200_OK)