from rest_framework import serializers

class IllustSerializer(serializers.Serializer):
    """
    イラストSerizalizer
    Attributes
    path : str
        画像パス
    """

    # 画像パス
    path = serializers.CharField()

class IllustListSerializer(serializers.ListSerializer):
    child = IllustSerializer()