import importlib

from django.core.management import call_command
import pytest
from pytest_mock import MockerFixture

from .create_setting_type_data import *

class Test__for_mock_target:

    def test__can_import_module_attribute(self):
        # WHEN
        module = importlib.import_module(SUT_MODULE_PATH)
        # THEN
        assert getattr(module, SETTING_HANDLE_FILE_PATH_ATTRIBUTE) is not None
        assert getattr(module, GET_SETTINGS_ATRRIBUTE) is not None


class TestCreateSettingType:

    class Test__write_type_def:

        command_name = 'create_setting_type'

        @pytest.mark.parametrize(
            'params',
            [
                pytest.param(data_setting.get_primitive(), id='primitive'),
                pytest.param(data_setting.get_sequence(), id='sequence'),
                pytest.param(data_setting.get_various_object(), id='various_object'),
            ]
        )
        def test__write_setting_handler(self, mocker: MockerFixture, params: ParamType):

            out_file_path, mock_dict, expected = params

            # Mock for setting file and path
            mocker.patch(f'{SUT_MODULE_PATH}.{SETTING_HANDLE_FILE_PATH_ATTRIBUTE}', out_file_path)
            mocker.patch(f'{SUT_MODULE_PATH}.{GET_SETTINGS_ATRRIBUTE}').return_value = MockSetting(mock_dict)

            # WHEN
            call_command(self.command_name)
            # THEN
            with (open(out_file_path, 'r')) as fr:
                assert fr.read() == expected