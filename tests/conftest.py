import os
from typing import List, Tuple, Dict, Optional, Any
import django
# importを解決する段階で設定ファイルが読み込み済である必要があるため、
# conftestのグローバル、すなわちテスト全体で最初に実行される部分に
# 依存モジュールの解決を定義
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
django.setup()

import pytest
import dataclasses
from _pytest.fixtures import SubRequest
from django.db import models
from rest_framework.test import APIClient

from common.api_response import SuccessAPIResponse

@dataclasses.dataclass
class ParamViewRequestType:
    """ View機能のテスト用パラメータ """
    client: APIClient
    path: str
    login_username: str
    model_items_list: List[List[models.Model]]
    expected_response: SuccessAPIResponse
    get_query: str = ''
    post_body: Optional[Dict[str, Any]] = None
    put_body: Optional[Dict[str, Any]] = None
    delete_body: Optional[Dict[str, Any]] = None


@pytest.fixture
def view_request_params(request: SubRequest) -> ParamViewRequestType:

    params: ParamViewRequestType = request.param

    # DB事前登録
    for model_items in params.model_items_list:
        [model.save() for model in model_items]

    return params