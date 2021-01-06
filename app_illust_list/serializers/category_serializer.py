from typing import Dict
from rest_framework.exceptions import ValidationError
from rest_framework import serializers

from app_illust_list.models.category import Category
from common.validator import is_unique_model

class CategorySerializer(serializers.Serializer):
    """
    カテゴリSerizalizer

    Attributes
    ----------
    category_name : str
        カテゴリ名
    """

    # カテゴリ名
    category_name = serializers.CharField(error_messages={'blank': 'カテゴリ名を入力してください。'})

    user_id = serializers.PrimaryKeyRelatedField(read_only=True)

    def validate_category_name(self, category_name: str) -> str:
        """ カテゴリ名バリデーション

        Parameters
        ----------
        value_dict : Dict[str, str]
            シリアライザから渡される入力値を格納した辞書

        Returns
        -------
        str
            後続の処理で扱えるよう、カテゴリ名文字列を返却

        Raises
        ------
        ValidationError
            ユニーク制約に反すると送出される
        """

        if not is_unique_model(Category, {'category_name': category_name}):

            raise ValidationError('カテゴリ名は既に使用されています。')
        
        return category_name

class CategoryListSerializer(serializers.ListSerializer):
    child = CategorySerializer()

