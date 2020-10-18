from rest_framework import serializers

class IllustDetailSerializer(serializers.Serializer):
    """
    イラスト詳細Serizalizer

    Attributes
    ----------
    path : str
        画像パス
    categories : List[str]
        カテゴリリスト
    """

    # 画像パス
    path = serializers.CharField()

    # 画像カテゴリ
    categories = serializers.ListField(
        child=serializers.CharField()
    )