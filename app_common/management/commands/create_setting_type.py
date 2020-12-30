from io import TextIOWrapper
from typing import Dict, Iterator

from django.core.management.base import BaseCommand
from django.conf import settings as conf_settings

from app_common.type_creator import TypeCreator, TypeCreateLogic
from app_common.type_handler import LINE_BREAK, TYPE_MODULE_IMPORT_LINE
from config import settings

# 設定ファイル格納パス
SETTINGS_HANDLE_FILE_PATH = './config/settings_handler.py'

def get_settings():
    """ 設定ファイルモジュールを取得 テスト時にモック化できるよう関数化

    Returns
    -------
    module
        設定ファイルモジュール
    """
    
    return settings

class SettingTypeCreateLogic(TypeCreateLogic):
    """ Django設定ファイル用型定義生成ロジック """

    def _get_setting_names(self) -> Iterator[str]:
        """ Djangoの設定ファイルから設定名のリストを取得

        Returns
        -------
        Iterator[str]
            設定ファイル名群
        """
        return filter(lambda setting: (not setting.startswith("__") and setting[0].isupper()), dir(get_settings()))

    def _get_setting_dict_text(self) -> str:
        """ 辞書形式で設定ファイルにアクセスするための辞書定義文字列を取得

        Returns
        -------
        str
            setting_dict: TypeSetting = {...}のような設定ファイル用辞書定義文字列
        """

        setting_names = self._get_setting_names()

        dict_start = f'setting_dict: TypeSetting = {{{LINE_BREAK}'
        dict_key_values = []
        for setting_name in setting_names:
            setting_value = getattr(get_settings(), setting_name)

            # 設定値が文字列であった場合、クォート無しで渡されるため、プログラム上で文字列として認識できるよう、再度クォートを付与
            if isinstance(setting_value,str):
                dict_key_values.append(f'    "{setting_name}": \'{setting_value}\',')
                continue

            dict_key_values.append(f'    "{setting_name}": {setting_value},')

        dict_end = f'{LINE_BREAK}}}'

        return f'{dict_start}{LINE_BREAK.join(dict_key_values)}{dict_end}'

    def _get_setting_dict(self) -> Dict:
        """ 設定ファイルの要素にアクセスするための辞書を取得

        Returns
        -------
        Dict
            設定ファイルの設定名・設定値を格納した辞書
        """

        setting_names = self._get_setting_names()
        setting_dict = {}

        for setting_name in setting_names:

            setting_value = getattr(get_settings(), setting_name)
            setting_dict[setting_name] = setting_value
        
        return setting_dict

    def write_type_def(self, f: TextIOWrapper):
        """ 設定ファイル用の型定義・設定ファイルへアクセスするための辞書文字列を出力

        Parameters
        ----------
        f : TextIOWrapper
            ファイル出力用
        """

        # import文
        f.write(TYPE_MODULE_IMPORT_LINE)
        f.write(LINE_BREAK)

        # 型エイリアス
        f.write(self.get_type_handler().dict.get_type_alias_text(self._get_setting_dict(), 'setting'))

        # 設定ファイル用辞書
        f.write(LINE_BREAK)
        f.write(self._get_setting_dict_text())
        f.write(LINE_BREAK)
        f.write(LINE_BREAK)

        # 外部から設定ファイル用辞書へアクセスするための関数
        f.write(f'def get_setting_dict() -> TypeSetting:{LINE_BREAK}')
        f.write('    return setting_dict')


class Command(BaseCommand):
    """ コマンドによって設定ファイル用型定義を生成 """

    def handle(self, *args, **options):
        """ コマンド実行により、Django設定ファイル用の型定義を生成 """
        creator = TypeCreator(SETTINGS_HANDLE_FILE_PATH, [SettingTypeCreateLogic()])
        creator.createTypeFile()