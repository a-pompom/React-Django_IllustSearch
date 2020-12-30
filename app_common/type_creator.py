import os

from io import TextIOWrapper
from typing import List

from .type_handler import TypeHandler

TYPE_HANDLER = TypeHandler()

class TypeCreateLogic():
    """ 型定義生成ロジック 型定義文字列をファイルへ出力 """

    def get_type_handler(self) -> TypeHandler:
        return TYPE_HANDLER

    def read_type_module(self, reader: TextIOWrapper):
        """ 型定義の生成元となるモジュールを読み込む

        Parameters
        ----------
        reader : TextIOWrapper
            型定義生成元ファイルを読み出した`もの
        """
        pass

    def write_type_def(self, writer: TextIOWrapper):
        """ 型定義文字列をファイルへ出力

        Parameters
        ----------
        writer : TextIOWrapper
            型定義生成用ファイルを読み出したもの
        """
        raise NotImplementedError() 
    
class TypeCreator:
    """ 型定義生成用クラス """

    def __init__(self, file_name: str, create_logic_list: List[TypeCreateLogic]):
        self._file_name = file_name
        self._logic_list = create_logic_list

    def createTypeFile(self):
        """ 型定義ファイルを生成
        ファイルを読み込んだ上での前処理・実際に型定義を書き込む処理を呼び出し 実際の処理はロジッククラスへ委譲
        """

        if os.path.exists(self._file_name):
            with open(self._file_name, 'r') as reader:
                [logic.read_type_module(reader) for logic in self._logic_list]

        with open(self._file_name, 'w') as writer:
            [logic.write_type_def(writer) for logic in self._logic_list]