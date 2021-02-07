from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from common.model import validator
from .models import User

USERNAME_MAX_LENGTH = 255

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

    # ユーザ名
    username = serializers.CharField(
        required = True,
        error_messages = {
            'blank': 'ユーザ名を入力してください'
        }
    )

    def validate_username(self, username: str) -> str:
        """ ユーザ名バリデーション
        文字種別・ユニークチェックを実行
        Returns
        -------
        username: str
            バリデーション後のユーザ名
        Raise
        -----
        ValidationError
            文字長・ユニーク性を満たさなかったときに送出される
        """

        # 文字長
        if not validator.is_valid_max_length(username, USERNAME_MAX_LENGTH):
            raise ValidationError(f'ユーザ名は{USERNAME_MAX_LENGTH}文字以下で入力してください。')

        # ユニーク
        if not validator.is_unique_model(User, {'username': username}):
            raise ValidationError('ユーザ名はすでに使用されています。')

        return username