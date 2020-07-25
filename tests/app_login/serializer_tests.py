import pytest

from app_login.serializer import LoginSerializer

class TestLoginSerializer:
    """ ログインAPI用Serializerのテスト 入力要素が存在するかのみを検証 """

    def test_初期状態にFieldとしてユーザ名が存在すること(self):

        # GIVEN
        login_serializer = LoginSerializer()

        # THEN
        assert login_serializer.get_fields()['username'] is not None