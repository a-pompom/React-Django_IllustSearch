import os
from typing import List, Tuple
import django
# importを解決する段階で設定ファイルが読み込み済である必要があるため、
# conftestのグローバル、すなわちテスト全体で最初に実行される部分に
# 依存モジュールの解決を定義
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
django.setup()

import pytest
from _pytest.fixtures import SubRequest
from django.db import models
from rest_framework.test import APIClient

from common.custom_type import TypeAPIResponse

ParamViewRequestType = Tuple[APIClient, str, str, List[List[models.Model]], TypeAPIResponse]


@pytest.fixture
def view_request_params(request: SubRequest) -> ParamViewRequestType:

    params: ParamViewRequestType = request.param
    client, path, username, model_items_list, expected = params

    # DB事前登録
    for model_items in model_items_list:
        [model.save() for model in model_items]

    return params