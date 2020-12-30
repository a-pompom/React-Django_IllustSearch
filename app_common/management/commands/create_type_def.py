import importlib
import os
from os.path import relpath

from io import TextIOWrapper
from typing import Any, List
from django.core.management.base import BaseCommand

from app_common.type_handler import LINE_BREAK, SEQUENCE_TYPES, TYPE_MODULE_IMPORT_LINE
from app_common.type_creator import TypeCreator, TypeCreateLogic

class TypeDefCreateLogic(TypeCreateLogic):
    """ 型定義文字列生成ロジック """

    # 型定義再生成時のマーカー
    TYPE_DEF_LINE = f'# TYPE DEF HERE{LINE_BREAK}'

    # 型定義生成対象オブジェクト トップレベルに記述すると、循環importが発生するため、
    # 型定義か生成元を毎回書き換えなければならない
    # 実際に使うときの記述量を最小限にするため、型定義生成対象を関数から取得し、
    # import文を関数内のブロックに閉じ込め、return文の記述からモジュール名を得るようにした
    TYPE_DEF_GET_STATEMENT = 'return'

    TYPE_DEF_MODULE_FUNCTION = 'get_type_def'

    def __init__(self):

        # 型定義までの文字列 型定義のみを再生成し、それ以前は毎回復元
        self._before_type_lines = []
        # 型定義生成対象オブジェクト
        self._modules: List[Any] = []
        # 型名
        self._module_names: List[str] = []

    def _set_module_names(self, module_def_text: str):
        """ モジュールの変数名を辞書型モジュールの型定義名に使えるよう保持

        Parameters
        ----------
        module_def_text : str
            'return [module1, module2]'形式の文字列
            リスト内の要素を抜き出す

        Example
        -------
        'return [module1, module2]' -> ['module1', 'module2']
        """

        module_names_text = module_def_text[module_def_text.index('[')+1:module_def_text.index(']')]
        self._module_names = module_names_text.replace(' ', '').split(',')
    
    def _get_type_import_text(self):
        """ 型ヒントimport文字列を生成 生成した型定義ファイルでSyntax Errorとならないようファイル先頭へ追記

        Returns
        -------
        str
            型ヒントimport文字列
        """

        module_def_text = ''.join(self._before_type_lines)
        # 二回目以降の生成では、既に型ヒントimport文字列が存在するので、スキップ
        if 'from typing' in module_def_text:
            return ''

        # import文とモジュールの間を1行空けるため、import文が存在しない場合は空行を挿入
        return f'{TYPE_MODULE_IMPORT_LINE}{LINE_BREAK}'

    def _get_module_type_def_text(self, module: Any, module_index: int) -> str:
        """ モジュールごとの型定義テキストを取得

        Parameters
        ----------
        module : Any
            対象モジュール
        module_index : int
            ファイルを読み出したときに取得したモジュール名を読み出すためのインデックス

        Returns
        -------
        str
            モジュールの型定義テキスト 型エイリアスで表現
        """

        type_handler = self.get_type_handler()

        # 辞書
        if type_handler.base._get_type_name(module) == 'dict':
            return type_handler.dict.get_type_alias_text(module, self._module_names[module_index])

        # シーケンス 
        if type_handler.base._get_type_name(module) in SEQUENCE_TYPES:

            # シーケンスの要素にディクショナリが含まれる場合、ディクショナリ自体にも型定義が必要
            # シーケンス内のディクショナリは、大抵匿名で、そのままでは型エイリアス名を決定できないので、
            # 他と重複する可能性の薄い、キーを結合した文字列を型エイリアス名とする
            if len(module) != 0 and type_handler.base._get_type_name(module[0]) == 'dict':

                joined_dict_key_name = '_'.join(module[0].keys())
                dict_type_def_text = type_handler.sequence.get_type_alias_text(module, self._module_names[module_index], joined_dict_key_name)
                return f'{type_handler.dict.get_type_alias_text(module[0], joined_dict_key_name)}{dict_type_def_text}'

            return type_handler.sequence.get_type_alias_text(module, self._module_names[module_index])

        # 型エイリアスの生成は不要と判定
        return ''

    def read_type_module(self, reader: TextIOWrapper):
        """ 型定義生成対象モジュールを読み出し

        Parameters
        ----------
        reader : TextIOWrapper
            型定義生成対象ファイルを読み出すためのTextIOWrapper
        """

        # path/module.py -> path.moduleとimport用文字列へ置き換えてimport
        type_module = importlib.import_module('.'.join(reader.name.replace('.py', '').split('/')))

        # 余計な型定義を出力しないよう、生成対象は限定
        self._modules = type_module.__getattribute__(self.TYPE_DEF_MODULE_FUNCTION)()

        # 型定義までのモジュール定義部分はそのままに、型定義部分を新たに出力するために読み出し
        for line in reader:
            if line == self.TYPE_DEF_LINE:
                break

            if self.TYPE_DEF_GET_STATEMENT in line:
                self._set_module_names(line)
            
            # 改行コードを持たない末尾行も他と同質とみなせるよう、改行コードを挿入
            # こうすることで、出力結果の冪等性を担保できる
            if LINE_BREAK not in line:
                line = f'{line}{LINE_BREAK}'
            
            self._before_type_lines.append(line)

    def write_type_def(self, writer: TextIOWrapper):
        """ 型定義を出力

        Parameters
        ----------
        writer : TextIOWrapper
            出力対象ファイルへ書き込むためのTextIOWrapper
        """

        # 型ヒントモジュールのimport文字列
        writer.write(self._get_type_import_text())
        
        # 元の型定義対象モジュールの復元
        for line in self._before_type_lines:
            writer.write(line)

        # 型定義の生成
        # 可読性を加味し、型定義とモジュール定義の間は1行空けておく
        if len(self._before_type_lines) > 0 and self._before_type_lines[-1] != LINE_BREAK:
            writer.write(LINE_BREAK)
        writer.write(f'{self.TYPE_DEF_LINE}')

        for index, mod in enumerate(self._modules):

            # 型定義文はネストしていても他と同質とみなせるよう、改行コードを含んでいる
            # 最後の型定義文にも改行コードが存在すると、終端行に不自然な空白が生じ、違和感が出てしまうので、終端行は改行コードを削除
            if index == len(self._modules) -1:
                line = self._get_module_type_def_text(mod, index)
                writer.write(line[:line.rfind(LINE_BREAK)])
                continue

            writer.write(self._get_module_type_def_text(mod, index))

def create_type_def(file_name: str):
    """ 型定義をファイルへ追記

    Parameters
    ----------
    file_name : str
        追記対象ファイル名
    """
    creator = TypeCreator(file_name, [TypeDefCreateLogic()])
    creator.createTypeFile()

def create_type_def_file(path):
    TYPE_SUFFIX = '_custom_type.py'
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(TYPE_SUFFIX):

                # pythonモジュールとしてimportできるよう、プロジェクトルートからのパスのみへ切り出し
                file_path = relpath(os.path.join(root, file), os.path.abspath(os.path.dirname(__name__)))

                # ex) ./dir/module_custom_type.py -> dir/module_custom_type.py
                print(file_path)
                create_type_def(file_path)
            
class Command(BaseCommand):
    """ コマンドによって設定ファイル用型定義を生成 """

    help = 'Djangoプロジェクト配下の、指定のパスを起点に末尾が「_custom_type.py」のファイルを対象に、型定義を生成します。'

    def add_arguments(self, parser):
        parser.add_argument(
            '--path', 
            help='Djangoプロジェクト配下の起点となるパスを指定します。ex) /app_login/types',
            type=str)

    def handle(self, *args, **options):
        """ コマンド実行により、Django設定ファイル用の型定義を生成 """

        # Djangoプロジェクトのアプリケーションが格納されているディレクトリを起点に型定義を生成
        os.chdir(os.path.dirname(os.path.realpath(__file__)))
        os.chdir('../../../')

        create_type_def_file(f'{os.getcwd()}{options["path"] if options["path"] is not None else ""}')