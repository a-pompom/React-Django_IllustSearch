import dataclasses
from typing import Dict, Any, List, Literal, Sequence, Tuple, cast

# 型
PRIMITIVE_TYPES = ('str', 'bool', 'int', 'float')
SEQUENCE_TYPES = ('list', 'tuple')
# 改行コード
LINE_BREAK = '\n'
# 型ヒントモジュールimport文
TYPE_MODULE_IMPORT_LINE = f'from typing import TypedDict, List, Tuple, Any{LINE_BREAK}'


class _BaseTypeHandler:
    """ 型定義生成処理の基本処理を格納したミックスイン """
    def _get_type_name(self, value: Any) -> str:
        """ 値の型名文字列を取得

        Parameters
        ----------
        value : Any
            型名取得対象文字列

        Returns
        -------
        str
            型名文字列
        """

        if type(value).__name__ == 'NoneType':
            return 'None'

        return type(value).__name__

    def _get_camel_type_var_name(self, expression: str) -> str:
        """ キャメルケースでのユーザ定義型名を取得

        Parameters
        ----------
        expression : str
            型名取得対象文字列

        Returns
        -------
        str
            ユーザ定義型名用文字列
        
        Example
        -------
        some_expression -> TypeSomeExpression
        """

        # 元の変数名表現の区切り文字を取得 .や_など一種の記号のみを想定
        def get_delimiter(string: str) -> str:
            symbols = filter(lambda s: not(s.isdigit() or s.isalpha()), string)
            return ''.join(set(symbols))

        delimiter = get_delimiter(expression)
        components = expression.split(delimiter) if delimiter else [expression]

        return f'Type{"".join([(component[0].upper() + component[1:]) for component in components])}'

class _SequenceTypeHandler(_BaseTypeHandler):
    """ シーケンスオブジェクト用の型定義生成ミックスイン """

    def get_type_annotation(self, source: Sequence, sequence_item_name: str='') -> str:
        """ シーケンス型アノテーション文字列を取得

        Parameters
        ----------
        source : Sequence
            生成元シーケンス
        sequence_item_name : str
            要素自体にも型アノテーションが必要な場合の、要素を識別するための名称

        Returns
        -------
        str
            <シーケンス型名>[<型名>]文字列

        Example
        -------
        [1,2,3] -> List[int], ('pom', 'kit') -> Tuple[str]
        """

        # シーケンスの型名部分を取得
        def get_sequence_type_name() -> str:
            if len(source) == 0:
                return 'Any'
            
            # 辞書型の場合は、ユーザ定義型とする
            if self._get_type_name(source[0]) == 'dict':
                return self._get_camel_type_var_name(f'{sequence_item_name}')

            # シーケンスの入れ子
            if self._get_type_name(source[0]) in SEQUENCE_TYPES:
                return self.get_type_annotation(cast(Sequence, source[0]), f'{sequence_item_name}')
            
            return self._get_type_name(source[0])
        
        # 型ヒントとして記述できるよう、list -> Listのように型名をCapital表記へ
        sequence_type_name = self._get_type_name(source)
        capital_sequence_type_name = f'{sequence_type_name[0].upper()}{sequence_type_name[1:]}'
        
        if self._get_type_name(source) != 'tuple':
            return f'{capital_sequence_type_name}[{get_sequence_type_name()}]'
        
        # Tupleの場合、要素数は固定なので、要素数分の型アノテーションを生成
        tuple_annotation = ', '.join(
            get_sequence_type_name() for _ in range(len(source))
            ) if len(source) != 0 else get_sequence_type_name()

        return f'{capital_sequence_type_name}[{tuple_annotation}]'

    def get_type_alias_text(self, source: Sequence, sequence_name: str, sequence_item_name: str='') -> str:
        """ シーケンスオブジェクト用型エイリアス宣言テキストを取得

        Parameters
        ----------
        source : Sequence
            生成対象シーケンス
        sequence_name : str
            生成対象シーケンス名
        sequence_item_name: str
            シーケンス内要素名 辞書は匿名であることが多く、そのままでは型エイリアス名が決まらないので、明示的に指定

        Returns
        -------
        str
            シーケンス用型エイリアス宣言テキスト
        """

        # シーケンスの中に辞書が含まれていると、匿名であることが多いので、シーケンス内の要素名が与えられている場合は、それを利用
        # ex) user = [{"name": "hoge"}] -> TypeUser = List[TypeName]
        #     get_type_alias_text(user, 'user', 'name')
        return (
            f'{self._get_camel_type_var_name(sequence_name)}'
            f' = '
            f'{self.get_type_annotation(source, sequence_item_name)}'
            f'{LINE_BREAK}'
        )


class _DictTypeHandler(_BaseTypeHandler):
    """ 辞書用の型定義生成ミックスイン """

    def _get_dict_value_type_name(self, value: Any) -> Literal['Dict', 'Sequence', 'SequenceDict', 'Other']:
        """ 辞書内の値の型名を取得

        Returns
        -------
        str
            値の型名文字列
        """
        if isinstance(value, dict):
            return 'Dict'
        
        is_sequence = isinstance(value, list) or isinstance(value, tuple)
        is_sequence_dict = is_sequence and len(value) > 0 and isinstance(value[0], dict)

        if is_sequence_dict:
            return 'SequenceDict'
        
        if is_sequence:
            return 'Sequence'
        
        return 'Other'

    def _get_inner_dict_list(self, source: Dict) -> List[Tuple[str, Dict]]:
        """ 辞書内の辞書のリストを取得 これをもとにネストした辞書にも型定義の生成を実行

        Parameters
        ----------
        source : Dict
            対象の辞書

        Returns
        -------
        List[Tuple[str, Dict]]
            ネストした辞書のキー, 値をタプル形式で格納したリスト ネストした辞書が無い場合は、空のリストが得られる
        """

        # 辞書内の辞書の型定義は、実際に型定義が参照される、外側の辞書よりも前に来る必要があるので、
        # insertで要素を追加
        inner_dict_list: List[Tuple[str, Dict]] = []

        for key, value in source.items():

            if self._get_dict_value_type_name(value) == 'Dict':                
                # 辞書の入れ子となっていた場合は、型名はユーザ定義となるので、キーをもとに生成
                inner_dict_list.insert(0, (key, value))
                inner_dict_list = self._get_inner_dict_list(value) + inner_dict_list
                continue

            if self._get_dict_value_type_name(value) == 'SequenceDict':
                inner_dict_list.insert(0, (key, value[0]))
                inner_dict_list = self._get_inner_dict_list(value[0]) + inner_dict_list
                continue
        
        return inner_dict_list

    def get_type_annotation(self, source: Dict, type_expression: Any) -> str:
        """ TypedDict型アノテーションを取得

        Parameters
        ----------
        source : Dict
            生成元ディクショナリ
        type_expression : Any
            辞書型の型名

        Returns
        ------
        str
            TypedDict("DictName", {...})のような型エイリアス文字列
        """

        type_var_name = self._get_camel_type_var_name(type_expression)
        items: List[str] = []
        for key, value in source.items():

            if self._get_dict_value_type_name(value) == 'Dict':                
                # 辞書の入れ子となっていた場合は、型名はユーザ定義となるので、キーをもとに生成
                items.append(f'"{key}": {self._get_camel_type_var_name(key)}')
                continue

            if self._get_dict_value_type_name(value) in ('Sequence', 'SequenceDict'):
                items.append(f'"{key}": {_SequenceTypeHandler().get_type_annotation(value, key)}')
                continue

            items.append(f'"{key}": {self._get_type_name(value)}')

        return f'TypedDict("{type_var_name}", {{ {", ".join(items)} }})'

    def get_type_alias_text(self, source: Dict, type_expression: Any) -> str:
        """ 辞書用の型エイリアス宣言文字列を取得

        Parameters
        ----------
        source : Dict
            生成対象辞書
        type_expression : Any
            辞書名表現

        Returns
        -------
        str
            辞書用の型エイリアス宣言文字列
        """

        inner_dict_list = self._get_inner_dict_list(source)

        # ex) TypeDict = TypedDict("TypeDict", {"key": value...}\n)
        current_dict_alias = (
            f'{self._get_camel_type_var_name(type_expression)}'
            f' = '
            f'{self.get_type_annotation(source, type_expression)}'
            f'{LINE_BREAK}'
        )

        # ネスト無しの辞書
        if not inner_dict_list:
            return current_dict_alias

        # ネストあり
        # TypeInnerDict = TypedDict(...)
        # TypeDict = TypedDict("TypeDict", {"inner_dict": TypeInnerDict})
        # といった形式で型エイリアステキストが生成される
        return LINE_BREAK.join(
            # value(dict), keyでネストした辞書用型エイリアス文字列を取得
            [(
                f'{self._get_camel_type_var_name(inner_dict[0])}'
                f' = '
                f'{self.get_type_annotation(inner_dict[1], inner_dict[0])}'
            ) for inner_dict in inner_dict_list
            ] +
            [current_dict_alias]
        )

@dataclasses.dataclass
class TypeHandler:
    """ 型定義生成処理用クラス """
    base: _BaseTypeHandler = _BaseTypeHandler()
    sequence: _SequenceTypeHandler = _SequenceTypeHandler()
    dict: _DictTypeHandler = _DictTypeHandler()