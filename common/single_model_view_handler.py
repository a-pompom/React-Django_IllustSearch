from typing import cast, Union, Tuple, Dict, Any, Callable, Type
from functools import wraps

from django.db.models.base import Model
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models.manager import BaseManager
from rest_framework.serializers import Serializer
from rest_framework.response import Response

from .api_response import api_response_handler
from config.messages import messages

def validate(view_func: Callable):
    """ 
    シリアライザを利用した更新処理に対する前処理として、バリデーションを実行

    Parameters
    ----------
    serializer : Serializer
        バリデーション対象のメソッド・値を格納したオブジェクト

    Returns
    -------
    Response
        更新結果を格納したAPIレスポンス
    """

    @wraps(view_func)
    def wrapper(self: Any, serializer: Serializer, *args) -> Response:
        if not serializer.is_valid():
            return api_response_handler.failure.render_validation_error(serializer.errors)

        return view_func(self, serializer, *args)
    return wrapper


class SingleModelViewHandler:
    """ 単一のModelを扱うViewの共通処理を定義
    """

    def __init__(self, view_key: str, serializer_class: Type[Serializer], model_class: Type[Model]):
        """ Viewと関連づけられたModel・シリアライザを格納

        Parameters
        ----------
        view_key : str
            エラーメッセージを取得する際に利用するView識別用文字列
        serializer_class : Type[Serializer]
            シリアライザクラス レスポンスでModelオブジェクトを格納したシリアライザインスタンスを生成するために利用
        model_class : Type[Model]
            Viewで操作する単一のModelクラス
        """

        self._view_key = view_key
        self._model_identifier_key = f'{view_key}_id'
        self._serializer_class = serializer_class
        self._model_class = model_class

    def _get_model_object(self, **query: Dict[str, str]) -> Tuple[Union[Model, None], str]:
        """ クエリをもとにDBへアクセスし、Modelオブジェクトを取得 クエリはカラム, 条件の辞書形式で記述

        Returns
        -------
        Tuple[Union[Model, None], str]
            Modelオブジェクト, エラーメッセージ
        """

        model_object = None

        try:
            model_manager: BaseManager[Any] = self._model_class.objects
            model_object = model_manager.get(**query)
        except ValidationError:
            return (None, 'invalid_uuid')
        except ObjectDoesNotExist:
            return (None, 'not_found')
        
        return (model_object, '')
    
    def _get_id_query(self, serializer: Serializer) -> Dict[str, str]:
        """ 識別子による絞り込み条件文字列を取得 """

        id = serializer.validated_data.get(f'{self._model_identifier_key}', '')
        return {
            f'{self._model_identifier_key}': id
        }


    @validate
    def post(self, serializer: Serializer, get_model_instance: Callable[[Serializer], Model]) -> Response:
        """ ユーザの入力値からModel→新規DBレコードを作成

        Parameters
        ----------
        serializer : Serializer
            入力値を格納したオブジェクト
        get_model_instance : Callable[[Serializer], Model]
            バリデーション後のシリアライザからModelのインスタンスを得るための関数

        Returns
        -------
        Response
            新規作成されたModelオブジェクトを格納したAPIレスポンス
        """

        model_object = get_model_instance(serializer)
        model_object.save()

        return api_response_handler.success.render_with_updated_model(self._view_key, self._serializer_class(instance=model_object))

    @validate
    def put(self, serializer: Serializer) -> Response:
        """ Modelの識別子から、既存レコードを更新

        Parameters
        ----------
        serializer : Serializer
            更新値を格納したオブジェクト

        Returns
        -------
        Response
            更新後のModelオブジェクトを格納したAPIレスポンス
        """

        model_object, error_key = self._get_model_object(**self._get_id_query(serializer))

        if model_object is None:
            return api_response_handler.failure.render_field_error(
                {self._model_identifier_key: [messages[self._view_key]['error']['update'][error_key]]}
            )

        # validated_data -> Model Attribute
        for key in serializer.validated_data:

            # 識別子は、対象の識別のためにシリアライザに含まれるが、更新する必要はないのでスキップ
            if 'id' in key:
                continue
            model_object.__setattr__(key, serializer.validated_data[key])
        
        model_object.save()

        return api_response_handler.success.render_with_updated_model(self._view_key, self._serializer_class(instance=model_object))

    @validate
    def delete(self, serializer: Serializer) -> Response:
        """ Modelの識別子をもとに、DBのレコードを削除

        Parameters
        ----------
        serializer : serializers.Serializer
            validation処理を実行するシリアライザ

        Returns
        -------
        Response
            APIレスポンス
        """

        model_object, error_key = self._get_model_object(**self._get_id_query(serializer))

        if model_object is None:
            return api_response_handler.failure.render_field_error(
                {self._model_identifier_key: [messages[self._view_key]['error']['delete'][error_key]]}
            )

        model_object.delete()

        return api_response_handler.success.render()


def get_single_model_view_handler(view_key: str, serializer_class: Type[Serializer], model_class: Type[Model]) -> SingleModelViewHandler:
    """ 各ViewごとのModel操作共通処理を取得

    Parameters
    ----------
    view_key : str
        エラーメッセージ取得用のView識別子
    serializer_class : Type[Serializer]
        レスポンスでViewごとのシリアライザを生成するためのクラス
    model_class : Type[Model]
        Model操作用クラス

    Returns
    -------
    SingleModelViewHandler
        共通処理を格納したハンドラ
    """
    return SingleModelViewHandler(view_key, serializer_class, model_class)