from __future__ import annotations

from django.db import models
from django.db.models import CharField
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.hashers import make_password

class User(AbstractBaseUser):
    """ 認証用ユーザ """

    class Meta:
        db_table = 'm_user'

    USERNAME_FIELD = 'username'

    # ユーザ名 ユニーク
    username: CharField[str, str] = models.CharField(
        name='username',
        max_length=255,
        unique=True,
    )

    # パスワード 今回のアプリでは使用せず、全ユーザ固定値
    password: CharField[str, str] = models.CharField(
        name='password',
        max_length=255,
        default=make_password('root')
    )

    # ユーザアイコンのパス
    icon_path: CharField[str, str] = models.CharField(
        name='icon_path',
        max_length=1024,
        null=True
    )

    def get_id(self) -> int:
        return int(self.pk)

    def __str__(self):

        return f'username: {self.username}'