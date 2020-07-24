from django.contrib.auth import login

from rest_framework import status, views
from rest_framework.request import Request
from rest_framework.response import Response

from .backend import AuthBackend
from .exception import LoginFailureException
from .models import User
from .serializer import LoginSerializer

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

        return Response(serializer.data, status=status.HTTP_200_OK)

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
        except LoginFailureException:

            return Response({'message': 'ユーザ名が間違っています。'}, status=status.HTTP_401_UNAUTHORIZED)

        # 認証処理で得られたユーザでセッションを発行
        login(request, user, 'app_login.backend.AuthBackend')

        # ログイン成功
        return Response({'message': 'ログイン成功'}, status=status.HTTP_200_OK)

        
