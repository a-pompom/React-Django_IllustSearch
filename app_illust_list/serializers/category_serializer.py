from rest_framework import serializers

class CategorySerializer(serializers.Serializer):
    """
    カテゴリSerizalizer

    Attributes
    ----------
    category_name : str
        カテゴリ名
    """

    # カテゴリ名
    category_name = serializers.CharField()

    user_id = serializers.CharField()

class CategoryListSerializer(serializers.ListSerializer):
    child = CategorySerializer()