from typing import Tuple, Union

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AnonymousUser
from rest_framework import status, views
from rest_framework.request import Request,HttpRequest
from rest_framework.response import Response

from common.login_user_handler import LoginRequiredMixin

from app_login.models import User

class DataGetLoginUserId:

    # DRFのRequest, 期待結果(ユーザID)
    ParamType = Tuple[Request, Union[int, None]]

    def _get_param(self, request: Request, expected: Union[int, None]) -> ParamType:
        return (
            request,
            expected
        )

    def get_specified_user_request(self) -> ParamType:

        expected = 1
        request = Request(HttpRequest())
        request.user = User(pk=expected)

        return self._get_param(request, expected)

    def get_anonymous_user_request(self) -> ParamType:

        expected = None
        request = Request(HttpRequest())
        request.user = AnonymousUser()

        return self._get_param(request, expected)


class MockView(LoginRequiredMixin, views.APIView):
    """ MixinからViewのメソッドを呼び出しているので、仲介用のテストViewを作成 """

    def __init__(self, user: Union[AbstractBaseUser, AnonymousUser]):
        self.user = user

    def get(self, request: Request) -> Response:
        return Response(request.user, status=status.HTTP_200_OK)


class DataInitial:

    # initial処理を呼び出すView, DRFのRequest(ユーザ情報を含む)
    ParamType = Tuple[MockView, Request]

    def _get_param(self, view: MockView, request: Request) -> ParamType:
        return (
            view,
            request
        )

    def _get_request(self, user: Union[AbstractBaseUser, AnonymousUser]) -> Request:
        """ Requestオブジェクトを取得 """
        
        http_request = HttpRequest()
        http_request.method = 'get'
        request = Request(http_request)
        request.user = user

        return request

    def get_specified_user_request(self) -> ParamType:

        user = User(pk=1, username='pompom')
        view = MockView(user)

        return self._get_param(view, self._get_request(user))

    def get_anonymous_user_request(self) -> ParamType:

        user = AnonymousUser()
        view = MockView(user)

        return self._get_param(view, self._get_request(user))


data_get_login_user_id = DataGetLoginUserId()
data_get_initial = DataInitial()