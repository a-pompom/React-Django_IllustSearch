from app_login.models import User
from django.shortcuts import render
from rest_framework import status, views
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Category, Illust
from .serializers import CategorySerializer, IllustSerializer

from common.api_response import APIResponseMixin
from common.user_handler import LoginUserHandlerMixin

class CategoryView(views.APIView, APIResponseMixin, LoginUserHandlerMixin):
    """ カテゴリAPI用View """

    def get(self, request: Request) -> Response:
        """ カテゴリ一覧表示

        Parameters
        ----------
        request : Request
            リクエスト情報 ユーザを識別するために利用

        Returns
        -------
        Response
            カテゴリ一覧を格納したレスポンス
        """

        category_list = Category.objects.filter(user_id = self.get_login_user_id(request)).order_by('-id')

        return Response(
            self.render_to_success_response(
                'ok',
                {
                    'category_list': CategorySerializer(instance=category_list, many=True).data
                }
            ),
            status=status.HTTP_200_OK
        )
    
class IllustView(views.APIView, APIResponseMixin, LoginUserHandlerMixin):
    """ イラストAPI用View """

    def get(self, request: Request) -> Response:
        """ イラスト一覧表示

        Parameters
        ----------
        request : Request
            リクエスト情報 ユーザを識別するために利用

        Returns
        -------
        Response
            イラスト一覧を格納したレスポンス
        """

        illust_list = Illust.objects.filter(user_id = self.get_login_user_id(request)).order_by('-id')

        return Response(
            self.render_to_success_response(
                'ok',
                {
                    'illust_list': IllustSerializer(instance=illust_list, many=True).data
                }
            ),
            status=status.HTTP_200_OK
        )