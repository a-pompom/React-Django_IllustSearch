from django.db.models import Max
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from rest_framework.exceptions import ErrorDetail
from rest_framework import status, views
from rest_framework.request import Request
from rest_framework.response import Response
from typing import cast

from .models import Category, Illust
from .serializers import CategorySerializer, IllustSerializer

from common.custom_type import TypeSerializerErrorDict
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
            user_id = login_user_handler.get_login_user(request)
        ).order_by('sort_order')

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
        """ カテゴリ新規登録

        Parameters
        ----------
        request : Request
            ボディへカテゴリ名を格納したリクエスト

        Returns
        -------
        Response
            登録結果 登録後のカテゴリオブジェクトも含む
        """
        
        category_serializer = CategorySerializer(data=request.data)

        # バリデーション
        if not category_serializer.is_valid():
            response = api_response_handler.render_to_error_response(
                '登録に失敗しました。', 
                cast(TypeSerializerErrorDict, category_serializer.errors)
            )

            return Response(response, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        sort_order = Category.objects.filter(user_id=login_user_handler.get_login_user(request)).aggregate(Max('sort_order'))['sort_order__max']
        category = Category(
            category_name=category_serializer.validated_data['category_name'],
            user_id=login_user_handler.get_login_user(request),
            sort_order=sort_order if sort_order is not None else 1
        )
        category.save()

        return Response(
            api_response_handler.render_to_success_response(
                'ok',
                {
                    'category': CategorySerializer(instance=category).data
                }
            ),
            status=status.HTTP_200_OK
        )

    def put(self, request: Request) -> Response:
        category_serializer = CategorySerializer(data=request.data, partial=True)

        # バリデーション
        if not category_serializer.is_valid():
            response = api_response_handler.render_to_error_response(
                '登録に失敗しました。', 
                cast(TypeSerializerErrorDict, category_serializer.errors)
            )

            return Response(response, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        
        try:
            category = Category.objects.get(category_id=category_serializer.validated_data.get('category_id', ''))
            category.category_name = category_serializer.validated_data['category_name']

            category.save()

            return Response(
                api_response_handler.render_to_success_response(
                    'ok',
                    {
                        'category': CategorySerializer(instance=category).data
                    }
                ),
                status=status.HTTP_200_OK
            )
        except ValidationError:
            response = api_response_handler.render_to_error_response(
                '登録に失敗しました。', 
                {'category_id': [ErrorDetail('カテゴリIDはUUID形式で指定してください。')]}
            )
            return Response(response, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        except ObjectDoesNotExist:
            response = api_response_handler.render_to_error_response(
                '登録に失敗しました。', 
                {'category_id': [ErrorDetail('更新対象のカテゴリが見つかりませんでした。')]}
            )
            return Response(response, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def delete(self, request: Request) -> Response:

        category_serializer = CategorySerializer(data=request.data, partial=True)

        if not category_serializer.is_valid():
            response = api_response_handler.render_to_error_response(
                '登録に失敗しました。',
                cast(TypeSerializerErrorDict, category_serializer.errors)
            )
            return Response(response, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        try:
            category: Category = Category.objects.get(category_id=category_serializer.validated_data.get('category_id', ''))
            category.delete()

            response = api_response_handler.render_to_success_response()
            return Response(response, status=status.HTTP_200_OK)

        except ValidationError:
            response = api_response_handler.render_to_error_response(
                '登録に失敗しました。', 
                {'category_id': [ErrorDetail('カテゴリIDはUUID形式で指定してください。')]}
            )
            return Response(response, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        except ObjectDoesNotExist:
            response = api_response_handler.render_to_error_response(
                '登録に失敗しました。', 
                {'category_id': [ErrorDetail('削除対象のカテゴリが見つかりませんでした。')]}
            )
            return Response(response, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


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
            'user_id': login_user_handler.get_login_user(request),
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