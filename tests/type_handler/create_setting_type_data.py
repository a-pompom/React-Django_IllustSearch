from typing import Tuple

from app_common.type_handler import LINE_BREAK, TYPE_MODULE_IMPORT_LINE
from tests.file_io_utils import IOTest

SUT_MODULE_PATH = 'app_common.management.commands.create_setting_type'
SETTING_HANDLE_FILE_PATH_ATTRIBUTE = 'SETTINGS_HANDLE_FILE_PATH'
GET_SETTINGS_ATRRIBUTE = 'get_settings'

class MockSetting: 
    def __init__(self, attrs: dict):
        self.attrs = attrs

    def __getattr__(self, name: str):
        return self.attrs[name]

    def __dir__(self):
        return self.attrs.keys()
    
# out_file_name, setting_mock_dict, expected
ParamType = Tuple[str, dict, str]
TEST_DATA_DIR = 'app_common/create_setting_type'

class DataSetting(IOTest):

    def _get_param(self, out_file_name: str, setting_mock_dict: dict, expected: str) -> ParamType:

        self._setup_for_write('', out_file_name)
        expected_text = LINE_BREAK.join([
            TYPE_MODULE_IMPORT_LINE,
            expected,
            '',
            'def get_setting_dict() -> TypeSetting:',
            '    return setting_dict'
        ])
        # 期待結果
        self._setup_for_write(expected_text, f'{out_file_name[:-3]}_expected.py')

        return (
            self._get_out_file_path(out_file_name),
            setting_mock_dict,
            expected_text,
        )
    
    # プリミティブ型
    def get_primitive(self) -> ParamType:

        mock_dict = {'VALUE': 'value'}

        expected = LINE_BREAK.join([
            'TypeSetting = TypedDict("TypeSetting", { "VALUE": str })',
            '',
            'setting_dict: TypeSetting = {',
            '    "VALUE": \'value\',',
            '}',
        ])

        return self._get_param(f'{TEST_DATA_DIR}/primitive.py', mock_dict, expected)

    # シーケンス
    def get_sequence(self) -> ParamType:

        mock_dict = {
            'NAME_LIST': ['pom', 'purin', 'john doe']
        }

        expected = LINE_BREAK.join([
            'TypeSetting = TypedDict("TypeSetting", { "NAME_LIST": List[str] })',
            '',
            'setting_dict: TypeSetting = {',
            '    "NAME_LIST": [\'pom\', \'purin\', \'john doe\'],',
            '}',
        ])

        return self._get_param(f'{TEST_DATA_DIR}/sequence.py', mock_dict, expected)

    # 辞書などを含むさまざまなオブジェクト
    def get_various_object(self) -> ParamType:

        mock_dict = {
            'IS_DEBUG': True,
            'ALLOWED_PORTS': (80, 443, 8080),
            'ADMIN_USERS': [{'name': 'pompom-purin', 'age': 100}, {'name': 'django', 'age': 3}],
        }

        expected = LINE_BREAK.join([
            'TypeADMINUSERS = TypedDict("TypeADMINUSERS", { "name": str, "age": int })',
            'TypeSetting = TypedDict("TypeSetting", { "ADMIN_USERS": List[TypeADMINUSERS], "ALLOWED_PORTS": Tuple[int, int, int], "IS_DEBUG": bool })',
            '',
            'setting_dict: TypeSetting = {',
            '    "ADMIN_USERS": [{\'name\': \'pompom-purin\', \'age\': 100}, {\'name\': \'django\', \'age\': 3}],',
            '    "ALLOWED_PORTS": (80, 443, 8080),',
            '    "IS_DEBUG": True,',
            '}',
        ])

        return self._get_param(f'{TEST_DATA_DIR}/various_object.py', mock_dict, expected)


data_setting = DataSetting()