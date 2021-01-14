import uuid

from django.db import models
from app_login.models import User

class Category(models.Model):
    """ イラストのカテゴリ """

    class Meta:
        db_table = 'm_category'

    # カテゴリ識別子
    category_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    # 作成ユーザID
    user_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False,
        db_column='user_id',
    )
    
    # カテゴリ名
    category_name = models.CharField(
        max_length=255,
        db_column='category_name',
    )

    # 表示順
    sort_order = models.IntegerField(
        db_column='sort_order',
        null=False,
        default=0
    )