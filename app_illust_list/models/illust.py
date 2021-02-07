import uuid

from django.db import models
from app_login.models import User
from .category import Category

class Illust(models.Model):
    """ 資料用イラスト """
    class Meta:
        db_table = 't_illust'

    # イラスト識別子
    illust_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    # 作成ユーザID
    # ユーザ削除時には、パスを参照して物理画像を削除していくので、DBのレコードは別途削除
    user_id = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        null = False,
        db_column='user_id',
    )

    # イラストと結びつくカテゴリ
    categories = models.ManyToManyField(Category)

    # 画像ファイルのパス
    path = models.TextField(
        db_column='path'
    )