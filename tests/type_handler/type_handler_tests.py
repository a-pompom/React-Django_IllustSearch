import pytest
from typing import Any

from app_common.type_handler import _BaseTypeHandler
from .type_handler_data import *

class Test__TypeHandler:

    class Test__BaseTypeHandler:

        class Test__get_type_name:

            @pytest.mark.parametrize(
                'value, expected',
                [
                    pytest.param(1970, 'int', id='primitive'),
                    pytest.param(None, 'None', id='none'),
                ]
            )
            def test__get_type_name(self, value: Any, expected: str):
                # WHEN
                sut = _BaseTypeHandler()
                actual = sut._get_type_name(value)
                # THEN
                assert actual == expected

        class Test__get_camel_type_name:

            @pytest.mark.parametrize(
                'value, expected', 
                [
                    pytest.param('user_defined_name', 'TypeUserDefinedName', id='snake_case'),
                    pytest.param('user.address.city', 'TypeUserAddressCity', id='dot_notation'),
                    pytest.param('user', 'TypeUser', id='no_delimiter')
                ]
            )
            def test__camel_case_type_alias_name(self, value: str, expected: str):
                # WHEN
                sut = _BaseTypeHandler()
                actual = sut._get_camel_type_var_name(value)
                # THEN
                assert actual == expected

    class Test__SequenceTypeHandler:

        class Test__get_type_annotation:

            @pytest.mark.parametrize(
                'params',
                [
                    pytest.param(data_sequence_annotation.get_empty_list(), id='empty'),
                    pytest.param(data_sequence_annotation.get_primitive_list(), id='primitive'),
                    pytest.param(data_sequence_annotation.get_dict_list(), id='dictionary'),
                ]
            )
            def test__list(self, params: DataSequenceAnnotationParamType):
                # GIVEN
                sut, source_list, list_name, expected = params
                # WHEN
                actual = sut.sequence.get_type_annotation(source_list, list_name)
                # THEN
                assert actual == expected

            @pytest.mark.parametrize(
                'params',
                [
                    pytest.param(data_sequence_annotation.get_empty_tuple(), id='empty'),
                    pytest.param(data_sequence_annotation.get_primitive_tuple(), id='primitive'),
                    pytest.param(data_sequence_annotation.get_dict_tuple(), id='dictionary'),
                ]
            )
            def test__tuple(self, params: DataSequenceAnnotationParamType):
                # GIVEN
                sut, source_tuple, tuple_name, expected = params
                # WHEN
                actual = sut.sequence.get_type_annotation(source_tuple, tuple_name)
                # THEN
                assert actual == expected

        class Test__get_type_alias_text:

            @pytest.mark.parametrize(
                'params',
                [
                    pytest.param(data_sequence_alias.get_empty_list(), id='empty'),
                    pytest.param(data_sequence_alias.get_primitive_list(), id='primitive'),
                    pytest.param(data_sequence_alias.get_dict_list(), id='dictionary'),
                ]
            )
            def test__list(self, params: DataSequenceAliasParamType):
                # GIVEN
                sut, source_list, list_name, list_item_name, expected = params
                # WHEN
                actual = sut.sequence.get_type_alias_text(source_list, list_name, list_item_name)
                # THEN
                assert actual == expected

            @pytest.mark.parametrize(
                'params',
                [
                    pytest.param(data_sequence_alias.get_empty_tuple(), id='empty'),
                    pytest.param(data_sequence_alias.get_primitive_tuple(), id='primitive'),
                    pytest.param(data_sequence_alias.get_dict_tuple(), id='dictionary'),
                ]
            )
            def test__tuple(self, params: DataSequenceAliasParamType):
                # GIVEN
                sut, source_tuple, tuple_name, tuple_item_name, expected = params
                # WHEN
                actual = sut.sequence.get_type_alias_text(source_tuple, tuple_name, tuple_item_name)
                # THEN
                assert actual == expected
        

    class Test__DictTypeHandler:

        class Test__get_type_annotation:

            @pytest.mark.parametrize(
                'params',
                [
                    pytest.param(data_dict_annotation.get_simple_dict(), id='simple'),
                    pytest.param(data_dict_annotation.get_nested_dict(), id='nested'),
                    pytest.param(data_dict_annotation.get_snake_case_dict(), id='snake_case_key'),
                ]
            )
            def test__various_dictionary(self, params: DataDictType):
                # GIVEN
                sut, source_dict, dict_name, expected = params
                # WHEN
                actual = sut.dict.get_type_annotation(source_dict, dict_name)
                # THEN
                assert actual == expected

        class Test__get_type_alias_text:

            @pytest.mark.parametrize(
                'params',
                [
                    pytest.param(data_dict_alias.get_simple_dict(), id='simple'),
                    pytest.param(data_dict_alias.get_nested_dict(), id='nested'),
                    pytest.param(data_dict_alias.get_snake_case_dict(), id='snake_case_key'),
                ]
            )
            def test__various_dictionary(self, params: DataDictType):
                # GIVEN
                sut, source_dict, dict_name, expected = params
                # WHEN
                actual = sut.dict.get_type_alias_text(source_dict, dict_name)
                # THEN
                assert actual == expected