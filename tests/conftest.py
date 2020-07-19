import pytest
import django
import os

# importを解決する段階で設定ファイルが読み込み済である必要があるため、
# conftestのグローバル、すなわちテスト全体で最初に実行される部分に
# 依存モジュールの解決を定義
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
django.setup()