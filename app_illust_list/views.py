from rest_framework import status, views
from rest_framework.request import Request
from rest_framework.response import Response

from app_login.models import User
from .models import Category, Illust
from .serializers import CategorySerializer, IllustSerializer

from common.api_response import api_response_handler
from common.request.pagination_handler import PaginationHandlerMixin
from common.login_user_handler import LoginRequiredMixin, login_user_handler

class CategoryView(LoginRequiredMixin, views.APIView):
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

        category_list = Category.objects.filter(
            user_id = login_user_handler.get_login_user_id(request)
        ).order_by('-id')

        return Response(
            api_response_handler.render_to_success_response(
                'ok',
                {
                    'category_list': CategorySerializer(instance=category_list, many=True).data
                }
            ),
            status=status.HTTP_200_OK
        )

    def post(self, request: Request) -> Response:
        
        category_serializer = CategorySerializer(data=request.data)
        category_serializer.is_valid()
        user = User.objects.get(id=category_serializer.validated_data['user_id'])
        category = Category(
            category_name=category_serializer.validated_data['category_name'],
            user_id=user,
        )
        category.save()

        return Response(
            api_response_handler.render_to_success_response(
                'ok',
                {
                    'category': category_serializer.data
                }
            ),
            status=status.HTTP_200_OK
        )


class IllustView(PaginationHandlerMixin, LoginRequiredMixin, views.APIView):
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

        query = {
            'id__gt': 2,
            'user_id': login_user_handler.get_login_user_id(request),
        }

        pagination = self.get_current_pagination(Illust, query, 5, ('-id',))
        illust_list = pagination['result_list']

        return Response(
            api_response_handler.render_to_success_response(
                'ok',
                {
                    'illust_list': IllustSerializer(instance=illust_list, many=True).data,
                    'has_next': pagination['has_next'],
                }
            ),
            status=status.HTTP_200_OK
        )