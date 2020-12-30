from typing import Sequence, Tuple

from app_common.type_handler import TypeHandler, LINE_BREAK

# sut, sequence for type annotation, sequence item name, expected
DataSequenceAnnotationParamType = Tuple[TypeHandler, Sequence, str, str]
# sut, sequence for type alias, sequence name, sequence item name, expected
DataSequenceAliasParamType = Tuple[TypeHandler, Sequence, str, str, str]
# sut, dict for type annotation/alias, dictionary_name, expected
DataDictType = Tuple[TypeHandler, dict, str, str]

class DataSequenceAnnotation:

    def _get_params(self, source_sequence: Sequence, sequence_item_name: str, expected: str) -> DataSequenceAnnotationParamType:
        return (
            TypeHandler(),
            source_sequence,
            sequence_item_name,
            expected,
        )

    # List
    def get_empty_list(self) -> DataSequenceAnnotationParamType:
        source = []
        expected = 'List[Any]'

        return self._get_params(source, '', expected)

    def get_primitive_list(self) -> DataSequenceAnnotationParamType:
        source = ['Smith', 'Andrew', 'PompomPurin']
        expected = 'List[str]'

        return self._get_params(source, '', expected)

    def get_dict_list(self) -> DataSequenceAnnotationParamType:
        source = [{'username': 'pom'}, {'username': 'purin'}]
        expected = 'List[TypeUser]'

        return self._get_params(source, 'user', expected)
    
    # Tuple
    def get_empty_tuple(self) -> DataSequenceAnnotationParamType:
        source = ()
        expected = 'Tuple[Any]'

        return self._get_params(source, '', expected)

    def get_primitive_tuple(self) -> DataSequenceAnnotationParamType:
        source = ('Smith', 'Andrew', 'PompomPurin')
        expected = 'Tuple[str, str, str]'

        return self._get_params(source, '', expected)

    def get_dict_tuple(self) -> DataSequenceAnnotationParamType:
        source = ({'username': 'pom'}, {'username': 'purin'})
        expected = 'Tuple[TypeUser, TypeUser]'

        return self._get_params(source, 'user', expected)


class DataSequenceAlias:

    def _get_params(self, source_sequence: Sequence, sequence_name: str, sequence_item_name: str, expected: str) -> DataSequenceAliasParamType:
        return (
            TypeHandler(),
            source_sequence,
            sequence_name,
            sequence_item_name,
            expected,
        )

    # List
    def get_empty_list(self) -> DataSequenceAliasParamType:
        source = []
        expected = f'TypeEmptyList = List[Any]{LINE_BREAK}'

        return self._get_params(source, 'empty_list', '', expected)

    def get_primitive_list(self) -> DataSequenceAliasParamType:
        source = ['Smith', 'Andrew', 'PompomPurin']
        expected = f'TypeNameList = List[str]{LINE_BREAK}'

        return self._get_params(source, 'name_list', '', expected)

    def get_dict_list(self) -> DataSequenceAliasParamType:
        source = [{'username': 'pom'}, {'username': 'purin'}]
        expected = f'TypeUserList = List[TypeUsername]{LINE_BREAK}'

        return self._get_params(source, 'user_list', 'username', expected)
    
    # Tuple
    def get_empty_tuple(self) -> DataSequenceAliasParamType:
        source = ()
        expected = f'TypeEmptyTuple = Tuple[Any]{LINE_BREAK}'

        return self._get_params(source, 'empty_tuple', '', expected)

    def get_primitive_tuple(self) -> DataSequenceAliasParamType:
        source = ('Smith', 'Andrew', 'PompomPurin')
        expected = f'TypeNameTuple = Tuple[str, str, str]{LINE_BREAK}'

        return self._get_params(source, 'name_tuple', '', expected)

    def get_dict_tuple(self) -> DataSequenceAliasParamType:
        source = ({'username': 'pom'}, {'username': 'purin'})
        expected = f'TypeUserTuple = Tuple[TypeUsername, TypeUsername]{LINE_BREAK}'

        return self._get_params(source, 'user_tuple', 'username', expected)

class DataDictAnnotation:

    def _get_params(self, source_dict: dict, dict_name: str, expected: str) -> DataDictType:
        return (
            TypeHandler(),
            source_dict,
            dict_name,
            expected,
        )

    # 単純な辞書
    def get_simple_dict(self) -> DataDictType:
        source_dict = {'username': 'pompom'}
        expected = 'TypedDict("TypeUser", { "username": str })'

        return self._get_params(source_dict, 'user', expected)

    # 辞書のネスト
    def get_nested_dict(self) -> DataDictType:
        source_dict = {
            'dog': {
                'leg': 4,
                'cuteness': 9999,
                'has_tail': True,
                'owner': {
                    'name': 'pompom',
                }
            },
            'cat': {
                'leg': 4,
                'dog': None,
                'cuteness': 'awesome',
            },
        }
        
        expected = 'TypedDict("TypeAnimalDic", { "dog": TypeDog, "cat": TypeCat })'

        return self._get_params(source_dict, 'animal_dic', expected)

    # ディクショナリのキーがスネークケース
    def get_snake_case_dict(self) -> DataDictType:

        source_dict = {
            'user_info': {
                'user_id': 1,
                'is_authenticated': False,
                'username': 'John Doe',
            }
        }

        expected ='TypedDict("TypeUser", { "user_info": TypeUserInfo })'
        
        return self._get_params(source_dict, 'user', expected)

class DataDictAlias:

    def _get_params(self, source_dict: dict, dict_name: str, expected: str) -> DataDictType:
        return (
            TypeHandler(),
            source_dict,
            dict_name,
            expected,
        )

    # 単純な辞書
    def get_simple_dict(self) -> DataDictType:
        source_dict = {'username': 'pompom'}
        expected = f'TypeUser = TypedDict("TypeUser", {{ "username": str }}){LINE_BREAK}'

        return self._get_params(source_dict, 'user', expected)

    # 辞書のネスト
    def get_nested_dict(self) -> DataDictType:
        source_dict = {
            'dog': {
                'leg': 4,
                'cuteness': 9999,
                'has_tail': True,
                'owner': {
                    'name': 'pompom',
                }
            },
            'cat': {
                'leg': 4,
                'dog': None,
                'cuteness': 'awesome',
            },
        }
        expected = LINE_BREAK.join([
            'TypeCat = TypedDict("TypeCat", { "leg": int, "dog": None, "cuteness": str })',
            'TypeOwner = TypedDict("TypeOwner", { "name": str })',
            'TypeDog = TypedDict("TypeDog", { "leg": int, "cuteness": int, "has_tail": bool, "owner": TypeOwner })',
            'TypeAnimalDic = TypedDict("TypeAnimalDic", { "dog": TypeDog, "cat": TypeCat })',
            ''
        ])

        return self._get_params(source_dict, 'animal_dic', expected)

    # ディクショナリのキーがスネークケース
    def get_snake_case_dict(self) -> DataDictType:

        source_dict = {
            'user_info': {
                'user_id': 1,
                'is_authenticated': False,
                'username': 'John Doe',
            }
        }

        expected = LINE_BREAK.join([
            'TypeUserInfo = TypedDict("TypeUserInfo", { "user_id": int, "is_authenticated": bool, "username": str })',
            'TypeUser = TypedDict("TypeUser", { "user_info": TypeUserInfo })',
            '',
        ])
        
        return self._get_params(source_dict, 'user', expected)


data_dict_annotation = DataDictAnnotation()
data_dict_alias = DataDictAlias()
data_sequence_annotation = DataSequenceAnnotation()
data_sequence_alias = DataSequenceAlias()