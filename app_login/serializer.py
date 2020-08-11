from rest_framework import serializers

class LoginSerializer(serializers.Serializer):
    """ ログインAPI用シリアライザ

    Attributes
    ----------
    username: CharField
        ログインユーザ名
    """

    # ユーザ名
    username = serializers.CharField(
        required = True,
        error_messages = {
            'blank': 'カテゴリ名を入力してください。'
        }
    )

class LoginListSerializer(serializers.ListSerializer):
    """ リストシリアライザ

    Attributes
    ----------
    child: LoginSerializer
        ログインシリアライザ
    """
    child = LoginSerializer()