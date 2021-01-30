from django.db.models import Max
from django.db.models.base import Model
from rest_framework import status, views
from rest_framework.request import Request
from rest_framework.response import Response

from rest_framework.serializers import Serializer

from .models import Category, Illust
from .serializers import CategorySerializer, IllustSerializer

from common.api_response import api_response_handler
from common.request.pagination_handler import PaginationHandlerMixin
from common.login_user_handler import LoginRequiredMixin, login_user_handler
from common.single_model_view_handler import get_single_model_view_handler


class CategoryView(LoginRequiredMixin, views.APIView):
    """ カテゴリAPI用View """

    def __init__(self):
        self._single_model_view_handler = get_single_model_view_handler('category', CategorySerializer, Category)

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
            user_id = login_user_handler.get_login_user(request)
        ).order_by('sort_order')

        return api_response_handler.success.render_with_body(
            {'category_list': CategorySerializer(instance=category_list, many=True).data}
        )

    def post(self, request: Request) -> Response:
        """ カテゴリ新規登録 """
        
        # バリデーション後のシリアライザから新規登録用Modelオブジェクトを生成
        def get_model_instance(serializer: Serializer) -> Model:

            sort_order = Category.objects.filter(user_id=login_user_handler.get_login_user(request)).aggregate(Max('sort_order'))['sort_order__max']
            return Category(
                category_name=serializer.validated_data['category_name'],
                user_id=login_user_handler.get_login_user(request),
                sort_order=sort_order if sort_order is not None else 1
            )

        return self._single_model_view_handler.post(
            CategorySerializer(data=request.data),
            get_model_instance
        )

    def put(self, request: Request) -> Response:
        """ カテゴリ更新 """
        return self._single_model_view_handler.put(
            CategorySerializer(data=request.data, partial=True)
        )

    def delete(self, request: Request) -> Response:
        """ カテゴリ削除 """
        return self._single_model_view_handler.delete(
            CategorySerializer(data=request.data, partial=True)
        )


# class IllustView(PaginationHandlerMixin, LoginRequiredMixin, views.APIView):
#     """ イラストAPI用View """

#     def get(self, request: Request) -> Response:
#         """ イラスト一覧表示

#         Parameters
#         ----------
#         request : Request
#             リクエスト情報 ユーザを識別するために利用

#         Returns
#         -------
#         Response
#             イラスト一覧を格納したレスポンス
#         """

#         query = {
#             'id__gt': 2,
#             'user_id': login_user_handler.get_login_user(request),
#         }

#         pagination = self.get_current_pagination(Illust, query, 5, ('-id',))
#         illust_list = pagination['result_list']

#         return Response(
#             api_response_handler.render_to_success_response(
#                 'ok',
#                 {
#                     'illust_list': IllustSerializer(instance=illust_list, many=True).data,
#                     'has_next': pagination['has_next'],
#                 }
#             ),
#             status=status.HTTP_200_OK
#         )