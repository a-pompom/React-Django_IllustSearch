from rest_framework import serializers

from .validator import clean_username

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
            'blank': ''
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

class SignupSerializer(serializers.Serializer):
    """ ユーザ登録API用シリアライザ

    Attributes
    ----------
    username: CharField
        登録用ユーザ名
    """

    class Meta:
        """ Formのcleanに相当 """
        validators = [clean_username]

    # ユーザ名
    username = serializers.CharField(
        required = True,
        error_messages = {
            'blank': 'ユーザ名を入力してください'
        }
    )
    