from typing import Callable, List, Tuple

from app_common.management.commands.create_type_def import TypeDefCreateLogic, create_type_def
from app_common.type_handler import LINE_BREAK, TYPE_MODULE_IMPORT_LINE
from tests.file_io_utils import IOTest

# テスト全体で扱うシンプルな入力文字列
SIMPLE_INPUT = [
    f'user = {{"username": "pompom"}}{LINE_BREAK}',
    f'def get_type_def():{LINE_BREAK}',
    '    return [user]'
]

TEST_DATA_DIR = 'type_def_handler'

# sut, ファイル印字文字列, 期待結果
TypeSut = Callable[[str], None]
ParamType = Tuple[TypeSut, str, str]
CommandParamType = Tuple[str, str]

# ファイル内容読み取り処理
class DataRead(IOTest):
    # 入力ファイル文字列, 出力ファイル名, 読み出し結果
    ParamType = Tuple[TypeDefCreateLogic, str, List[str]]
    sut = TypeDefCreateLogic()

    def _get_params(self, in_file_text: str, out_file_name: str, expected: List[str]) -> ParamType:

        self._setup_for_write(in_file_text, out_file_name)
        return (
            self.sut,
            self._get_out_file_path(out_file_name),
            expected,
        )
    
    # シンプルなディクショナリによる入力文字列
    def get_input_text_for_simple_dict(self) -> ParamType:

        expected: List[str] = [SIMPLE_INPUT[0], SIMPLE_INPUT[1], f'{SIMPLE_INPUT[2]}{LINE_BREAK}']

        return self._get_params(''.join(SIMPLE_INPUT), f'{TEST_DATA_DIR}/read_simple_dict.py', expected)


# ファイルへの書き込みのみ
class DataWrite:

    # sut, 出力文字列
    ParamType = Tuple[TypeDefCreateLogic, str]
    sut = TypeDefCreateLogic()

    def _get_params(self, expected: str) -> ParamType:
        return (
            self.sut,
            expected,
        )

    # 型定義文字のみ
    def get_only_writing_text(self) -> ParamType:

        # 期待結果組み立て
        expected: str = LINE_BREAK.join([
            f'{TypeDefCreateLogic.TYPE_DEF_LINE}',
        ])
        expected = f'{TYPE_MODULE_IMPORT_LINE}{LINE_BREAK}{expected}'
        
        return self._get_params(expected)


# ファイルの入出力(ディクショナリ)
class DataReadAndWrite(IOTest):

    def _get_params(self, out_file_name: str, input: str, expected: str) -> ParamType:

        expected_text = f'{TYPE_MODULE_IMPORT_LINE}{LINE_BREAK}{input}{LINE_BREAK}{LINE_BREAK}{TypeDefCreateLogic.TYPE_DEF_LINE}{expected}'

        # 実際の処理結果
        self._setup_for_write(input, out_file_name)
        # 期待結果
        self._setup_for_write(expected_text, f'{out_file_name[:-3]}_expected.py')

        return (
            create_type_def,
            self._get_out_file_path(out_file_name),
            expected_text
        )
    
    # 単純な辞書用のテストデータ
    def get_output_text_for_simple_dict(self) -> ParamType:

        # 入力
        input = LINE_BREAK.join([
            'user = {"username": "pompom"}',
            'def get_type_def():',
            '    return [user]',
        ])

        # 期待結果組み立て
        expected: str = LINE_BREAK.join([
            'TypeUser = TypedDict("TypeUser", { "username": str })',
        ])

        return self._get_params(f'{TEST_DATA_DIR}/simple_dict.py', input, expected)

    # ネストした辞書を持つテストデータ
    def get_output_text_for_multiple_nested_dict(self) -> ParamType:

        # 入力
        input: str = LINE_BREAK.join([
            'response = { "body": { "message": "success", "status_code": 200}, "has_error": False }',
            'user = {"username": "pompom", "age": 100,} ',
            'def get_type_def():',
            '    return [response, user]',
        ])

        # 期待結果組み立て
        expected: str = LINE_BREAK.join([
            'TypeBody = TypedDict("TypeBody", { "message": str, "status_code": int })',
            'TypeResponse = TypedDict("TypeResponse", { "body": TypeBody, "has_error": bool })',
            'TypeUser = TypedDict("TypeUser", { "username": str, "age": int })',
        ])

        return self._get_params(f'{TEST_DATA_DIR}/nested_dict.py', input, expected)

    # 辞書内にリストを持つテストデータ
    def get_output_text_for_list_dict(self) -> ParamType:

        # 入力
        input: str = LINE_BREAK.join([
            'user = {"username": "pompom", "tel": ["000-0000", "123-4567"]}',
            'characters_dict = {"characters": [{"name": "purin", "has_twitter_acount": False,}, {"name": "kitty", "has_twitter_acount": True,}]}',
            'def get_type_def():',
            '    return [user, characters_dict]'
        ])

        # 期待結果組み立て
        expected: str = LINE_BREAK.join([
            'TypeUser = TypedDict("TypeUser", { "username": str, "tel": List[str] })',
            'TypeCharacters = TypedDict("TypeCharacters", { "name": str, "has_twitter_acount": bool })',
            'TypeCharactersDict = TypedDict("TypeCharactersDict", { "characters": List[TypeCharacters] })',
        ])

        return self._get_params(f'{TEST_DATA_DIR}/list_dict.py', input, expected)

    # 辞書内にタプルを持つテストデータ
    def get_output_text_for_tuple_dict(self) -> ParamType:
        # 入力
        input: str = LINE_BREAK.join([
            'user = {"username": "pompom", "tel": ("000-0000", "123-4567")}',
            'characters_dict = {"characters": ({"name": "purin", "has_twitter_acount": False,}, {"name": "kitty", "has_twitter_acount": True,})}',
            'def get_type_def():',
            '    return [user, characters_dict]',
        ])

        # 期待結果組み立て
        expected: str = LINE_BREAK.join([
            'TypeUser = TypedDict("TypeUser", { "username": str, "tel": Tuple[str, str] })',
            'TypeCharacters = TypedDict("TypeCharacters", { "name": str, "has_twitter_acount": bool })',
            'TypeCharactersDict = TypedDict("TypeCharactersDict", { "characters": Tuple[TypeCharacters, TypeCharacters] })',
        ])

        return self._get_params(f'{TEST_DATA_DIR}/tuple_dict.py', input, expected)

    # 外部モジュールから型定義を生成するためのテストデータ
    def get_output_text_for_external_module(self) -> ParamType:

        # 外部モジュールの作成
        external_module_text = LINE_BREAK.join([
            'user = {"username": "pompom-purin", "is_authenticated": False}'
        ])
        self._setup_for_write(external_module_text, f'{TEST_DATA_DIR}/test_module.py')

        # 入力
        input = LINE_BREAK.join([
            'def get_type_def():',
            '    from .test_module import user',
            '    return [user]',
        ])
        
        # 期待結果
        expected = LINE_BREAK.join([
            'TypeUser = TypedDict("TypeUser", { "username": str, "is_authenticated": bool })',
        ])

        return self._get_params(f'{TEST_DATA_DIR}/external_module.py', input, expected)


# シーケンス
class DataReadAndWriteForSequence(IOTest):

    def _get_params(self, out_file_name: str, input: str, expected: str) -> ParamType:

        expected_text = f'{TYPE_MODULE_IMPORT_LINE}{LINE_BREAK}{input}{LINE_BREAK}{LINE_BREAK}{TypeDefCreateLogic.TYPE_DEF_LINE}{expected}'

        # 実際の処理結果
        self._setup_for_write(input, out_file_name)
        # 期待結果
        self._setup_for_write(expected_text, f'{out_file_name[:-3]}_expected.py')
        return (
            create_type_def,
            self._get_out_file_path(out_file_name),
            expected_text
        )

    # 単純なリスト用
    def get_output_text_for_simple_list(self) -> ParamType:

        # 入力
        input = LINE_BREAK.join([
            'fruits = ["apple", "banana"]',
            'def get_type_def():',
            '    return [fruits]',
        ])

        # 期待結果組み立て
        expected: str = LINE_BREAK.join([
            'TypeFruits = List[str]',
        ])

        return self._get_params(f'{TEST_DATA_DIR}/sequence/simple_list.py', input, expected)

    def get_output_text_for_simple_tuple(self) -> ParamType:

        # 入力
        input = LINE_BREAK.join([
            'fruits = ("apple", "banana")',
            'def get_type_def():',
            '    return [fruits]',
        ])

        # 期待結果組み立て
        expected: str = LINE_BREAK.join([
            'TypeFruits = Tuple[str, str]',
        ])

        return self._get_params(f'{TEST_DATA_DIR}/sequence/simple_tuple.py', input, expected)

    # ディクショナリのリスト
    def get_output_text_for_dictionary_list(self) -> ParamType:

        # 入力
        input = LINE_BREAK.join([
            'users = [{"username": "pompom", "user_age": 100}, {"username": "purin", "user_age": 0}]',
            'def get_type_def():',
            '    return [users]',
        ])

        # 期待結果組み立て
        expected: str = LINE_BREAK.join([
            'TypeUsernameUserAge = TypedDict("TypeUsernameUserAge", { "username": str, "user_age": int })',
            'TypeUsers = List[TypeUsernameUserAge]',
        ])

        return self._get_params(f'{TEST_DATA_DIR}/sequence/dictionary_list.py', input, expected)

    def get_output_text_for_nested_list(self) -> ParamType:

        # 入力
        input = LINE_BREAK.join([
            'address_list = [["Hiroshima-1-1", "Hiroshima-2-2"], ["Tokyo-0-0", "Tokyo-10-0"]]',
            'def get_type_def():',
            '    return [address_list]'
        ])

        # 期待結果組み立て
        expected = LINE_BREAK.join([
            'TypeAddressList = List[List[str]]'
        ])

        return self._get_params(f'{TEST_DATA_DIR}/sequence/nested_list.py', input, expected)


class DataReadAndWriteCommand(IOTest):

    def _get_params(self, out_file_name: str, input: str, expected: str) -> CommandParamType:

        expected_text = f'{TYPE_MODULE_IMPORT_LINE}{LINE_BREAK}{input}{LINE_BREAK}{LINE_BREAK}{TypeDefCreateLogic.TYPE_DEF_LINE}{expected}'

        # 実際の処理結果
        self._setup_for_write(input, out_file_name)
        # 期待結果
        self._setup_for_write(expected_text, f'{out_file_name[:-3]}_expected.py')
        return (
            self._get_out_file_path(out_file_name),
            expected_text
        )

    def _get_excluded_params(self, out_file_name: str, input: str) -> CommandParamType:

        self._setup_for_write(input, out_file_name)
        self._setup_for_write(input, f'{out_file_name[:-3]}_expected.py')

        return (
            self._get_out_file_path(out_file_name),
            input
        )

    # ファイルが対象となるかが重要なので、中身はシンプルにしておく
    def get_output_text_no_argument(self) -> CommandParamType:

        # 入力
        input = LINE_BREAK.join([
            'fruits = ["apple", "banana"]',
            'user = {"name": "pompom", "age": 100}',
            'def get_type_def():',
            '    return [fruits, user]',
        ])

        # 期待結果組み立て
        expected: str = LINE_BREAK.join([
            'TypeFruits = List[str]',
            'TypeUser = TypedDict("TypeUser", { "name": str, "age": int })',
        ])

        return self._get_params(f'test_types/no_argument_custom_type.py', input, expected)

    def get_output_text_excluded(self) -> CommandParamType:
        # 入力
        input = LINE_BREAK.join([
            'fruits = ["apple", "banana"]',
            'user = {"name": "pompom", "age": 100}',
            'def get_type_def():',
            '    return [fruits, user]',
        ])

        return self._get_excluded_params(f'test_types/exclude.py', input)

    def get_output_text_parent(self) -> CommandParamType:
        # 入力
        input = LINE_BREAK.join([
            'fruits = ["apple", "banana"]',
            'user = {"name": "pompom", "age": 100}',
            'def get_type_def():',
            '    return [fruits, user]',
        ])

        return self._get_excluded_params(f'test_types/parent_custom_type.py', input)

    def get_output_text_child(self) -> CommandParamType:

        # 入力
        input = LINE_BREAK.join([
            'fruits = ["apple", "banana"]',
            'user = {"name": "pompom", "age": 100}',
            'def get_type_def():',
            '    return [fruits, user]',
        ])

        # 期待結果組み立て
        expected: str = LINE_BREAK.join([
            'TypeFruits = List[str]',
            'TypeUser = TypedDict("TypeUser", { "name": str, "age": int })',
        ])

        return self._get_params(f'test_types/child/child_custom_type.py', input, expected)


data_read = DataRead()
data_write = DataWrite()
data_read_and_write = DataReadAndWrite()
data_read_and_write_for_sequence = DataReadAndWriteForSequence()
data_read_and_write_for_command = DataReadAndWriteCommand()