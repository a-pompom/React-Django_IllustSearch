from django.db import models
from app_login.models import User

class Category(models.Model):
    """ イラストのカテゴリ """

    class Meta:
        db_table = 'm_category'

    # 作成ユーザID
    user_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null = False,
        db_column='user_id',
    )
    
    # カテゴリ名
    category_name = models.CharField(
        max_length=255,
        db_column='category_name',
    )