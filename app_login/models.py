from __future__ import annotations
import uuid

from django.db import models
from django.db.models import CharField
from django.contrib.auth.models import AbstractBaseUser

class User(AbstractBaseUser):
    """ 認証用ユーザ """

    class Meta:
        db_table = 'm_user'

    USERNAME_FIELD = 'username'

    # ユーザ識別子
    user_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

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
    )

    # ユーザアイコンのパス
    icon_path: CharField[str, str] = models.CharField(
        name='icon_path',
        max_length=1024,
        null=True
    )

    def get_id(self) -> str:
        return self.user_id

    def __str__(self):

        return f'username: {self.username}'