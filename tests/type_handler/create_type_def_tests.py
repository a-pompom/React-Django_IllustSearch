from pathlib import Path
import pytest

from django.core.management import call_command

from .create_type_def_data import *

class TestCreateTypeDef:

    class Test__read_type_def:

        def test__read_before_type_def(self):
            
            # GIVEN
            sut, in_file_name, expected_text = data_read.get_input_text_for_simple_dict()
            # WHEN
            with open(in_file_name, 'r') as r:
                sut.read_type_module(r)
            # THEN
            assert all(actual == expected for actual, expected in zip(sut._before_type_lines, expected_text))

    class Test__write_type_def:
        
        def test__write_only_type_def(self, tmp_path: Path):

            # GIVEN
            sut, expected = data_write.get_only_writing_text()
            tmp_file = tmp_path / 'empty.py'
            # WHEN
            sut.write_type_def(tmp_file.open('w'))
            # THEN
            assert tmp_file.read_text() == expected

    class Test__create_type_def:

        @pytest.mark.parametrize(
            'params',
            [
                pytest.param(data_read_and_write.get_output_text_for_simple_dict(), id='simple'),
                pytest.param(data_read_and_write.get_output_text_for_multiple_nested_dict(), id='nested'),
                pytest.param(data_read_and_write.get_output_text_for_external_module(), id='import'),
                pytest.param(data_read_and_write.get_output_text_for_list_dict(), id='list_dict'),
                pytest.param(data_read_and_write.get_output_text_for_tuple_dict(), id='tuple_dict'),
            ]
        )
        def test__dict(self, params: ParamType):
            # GIVEN
            sut, out_file_name, expected = params
            # WHEN
            sut(out_file_name)
            # THEN
            with open(out_file_name, 'r') as fr:
                assert fr.read() == expected

        def test__multiple_creation(self):

            # GIVEN
            sut, out_file_name, expected = data_read_and_write.get_output_text_for_simple_dict()
            # WHEN
            sut(out_file_name)
            sut(out_file_name)
            sut(out_file_name)
            # THEN
            with open(out_file_name, 'r') as fr:
                assert fr.read() == expected


    class Test__create_type_def_Sequence:

        @pytest.mark.parametrize(
            'params',
            [
                pytest.param(data_read_and_write_for_sequence.get_output_text_for_simple_list(), id='simple_list'),
                pytest.param(data_read_and_write_for_sequence.get_output_text_for_dictionary_list(), id='dictionary_list'),
                pytest.param(data_read_and_write_for_sequence.get_output_text_for_nested_list(), id='nested_list'),
                pytest.param(data_read_and_write_for_sequence.get_output_text_for_simple_tuple(), id='simple_tuple'),
            ]
        )
        def test__sequence(self, params: ParamType):
            # GIVEN
            sut, out_file_name, expected = params
            # WHEN
            sut(out_file_name)
            # THEN
            with open(out_file_name, 'r') as fr:
                assert fr.read() == expected

    
    class Test__create_type_def_file:

        command_name = 'create_type_def'

        def test__no_argument(self):
            # GIVEN
            out_file_name, expected = data_read_and_write_for_command.get_output_text_no_argument()
            # WHEN
            call_command(self.command_name)
            # THEN
            with open(out_file_name, 'r') as fr:
                assert fr.read() == expected

        def test__excluded_file(self):
            # GIVEN
            out_file_name, expected = data_read_and_write_for_command.get_output_text_excluded()
            # WHEN
            call_command(self.command_name)
            # THEN
            with open(out_file_name, 'r') as fr:
                assert fr.read() == expected

        def test__with_argument(self):
            # GIVEN
            out_file_name_parent, expected_parent = data_read_and_write_for_command.get_output_text_parent()
            out_file_name_child, expected_child = data_read_and_write_for_command.get_output_text_child()
            # WHEN
            call_command(self.command_name, *[], **{'path': '/tests/test_data/test_types/child'})
            # THEN
            with open(out_file_name_parent, 'r') as fr:
                assert fr.read() == expected_parent
            # THEN
            with open(out_file_name_child, 'r') as fr:
                assert fr.read() == expected_child