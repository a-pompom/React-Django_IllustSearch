import pytest
from pytest_mock import MockerFixture
from rest_framework.status import HTTP_200_OK, HTTP_422_UNPROCESSABLE_ENTITY

from app_illust_list.models.category import Category
from .category_view_data import MOCK_CATEGORY_UUID_LIST, data_get, data_post, data_put, data_delete, get_path
from tests.view_utils import test_common_view_function
from tests.conftest import ParamViewRequestType

# Viewテスト用パラメータ名
VIEW_REQUEST_PARAMS = 'view_request_params'
UUID_MOCK_MODULE_NAME = 'uuid.uuid4'


@pytest.mark.django_db(transaction=False)
class TestCategoryView:

    def test__common(self):
        test_common_view_function.run_tests({'login_path': get_path()})


    class Test__get:

        @pytest.mark.parametrize(
            VIEW_REQUEST_PARAMS,
            [
                pytest.param(data_get.get_success_get(), id='simple')
            ],
            indirect=[VIEW_REQUEST_PARAMS]
        )
        def test__get_categories(self, view_request_params: ParamViewRequestType):

            # GIVEN
            params = view_request_params
            client, path, username, expected = (params.client, params.path, params.login_username, params.expected_response)
            # WHEN
            client.login(username=username)
            actual = client.get(path)
            # THEN
            assert actual.status_code == HTTP_200_OK
            assert actual.data == expected


    class Test__post:

        @pytest.mark.parametrize(
            VIEW_REQUEST_PARAMS,
            [
                pytest.param(data_post.get_single_category(), id='simple')
            ],
            indirect=[VIEW_REQUEST_PARAMS]
        )
        def test__create_category(self, view_request_params: ParamViewRequestType):
            # GIVEN
            params = view_request_params
            client, path, username, post_body, expected = (params.client, params.path, params.login_username, params.post_body, params.expected_response)
            # WHEN
            client.login(username=username)
            actual = client.post(path, post_body)
            actual.data['body']['category']['category_id'] = ''
            # THEN
            assert actual.status_code == HTTP_200_OK
            assert actual.data == expected

        @pytest.mark.parametrize(
            VIEW_REQUEST_PARAMS,
            [
                pytest.param(data_post.get_empty_category_post(), id='simple')
            ],
            indirect=[VIEW_REQUEST_PARAMS]
        )
        def test__empty(self, view_request_params: ParamViewRequestType):
            # GIVEN
            params = view_request_params
            client, path, username, post_body, expected = (params.client, params.path, params.login_username, params.post_body, params.expected_response)
            # WHEN
            client.login(username=username)
            actual = client.post(path, post_body)
            # THEN
            assert actual.status_code == HTTP_422_UNPROCESSABLE_ENTITY
            assert actual.data == expected

        @pytest.mark.parametrize(
            VIEW_REQUEST_PARAMS,
            [
                pytest.param(data_post.get_duplicate_category_post(), id='simple')
            ],
            indirect=[VIEW_REQUEST_PARAMS]
        )
        def test__duplicate(self, view_request_params: ParamViewRequestType):
            # GIVEN
            params = view_request_params
            client, path, username, post_body, expected = (params.client, params.path, params.login_username, params.post_body, params.expected_response)
            # WHEN
            client.login(username=username)
            # 二重登録となるよう、二回Post
            client.post(path, post_body)
            actual = client.post(path, post_body)
            # THEN
            assert actual.status_code == HTTP_422_UNPROCESSABLE_ENTITY
            assert actual.data == expected


    class Test__put:
        
        @pytest.mark.parametrize(
            VIEW_REQUEST_PARAMS,
            [
                pytest.param(data_put.get_single_category_put(), id='simple')
            ],
            indirect=[VIEW_REQUEST_PARAMS]
        )
        def test__update_category(self, view_request_params: ParamViewRequestType):
            # GIVEN
            params = view_request_params
            client, path, username,  put_body, expected = (params.client, params.path, params.login_username, params.put_body, params.expected_response)
            # WHEN
            client.login(username=username)
            actual = client.put(path, put_body)
            # THEN
            assert actual.status_code == HTTP_200_OK
            assert actual.data == expected
        
        @pytest.mark.parametrize(
            VIEW_REQUEST_PARAMS,
            [
                pytest.param(data_put.get_empty_category_name_put(), id='empty')
            ],
            indirect=[VIEW_REQUEST_PARAMS]
        )
        def test__empty_category_name(self, view_request_params: ParamViewRequestType):
            # GIVEN
            params = view_request_params
            client, path, username,  put_body, expected = (params.client, params.path, params.login_username, params.put_body, params.expected_response)
            # WHEN
            client.login(username=username)
            actual = client.put(path, put_body)
            # THEN
            assert actual.status_code == HTTP_422_UNPROCESSABLE_ENTITY
            assert actual.data == expected

        @pytest.mark.parametrize(
            VIEW_REQUEST_PARAMS,
            [
                pytest.param(data_put.get_empty_category_id_put(), id='empty_category_id')
            ],
            indirect=[VIEW_REQUEST_PARAMS]
        )
        def test__empty_category_id(self, view_request_params: ParamViewRequestType):
            # GIVEN
            params = view_request_params
            client, path, username, put_body, expected = (params.client, params.path, params.login_username, params.put_body, params.expected_response)
            # WHEN
            client.login(username=username)
            actual = client.put(path, put_body)
            # THEN
            assert actual.status_code == HTTP_422_UNPROCESSABLE_ENTITY
            assert actual.data == expected

    
    class Test__delete:

        @pytest.mark.parametrize(
            VIEW_REQUEST_PARAMS,
            [
                pytest.param(data_delete.get_single_category_delete(), id='simple')
            ],
            indirect=[VIEW_REQUEST_PARAMS]
        )
        def test__success_delete(self, view_request_params: ParamViewRequestType):
            # GIVEN
            params = view_request_params
            client, path, username, delete_body, expected = (params.client, params.path, params.login_username, params.delete_body, params.expected_response)
            # WHEN
            client.login(username=username)
            actual = client.delete(path, delete_body)
            # THEN
            assert actual.status_code == HTTP_200_OK
            assert actual.data == expected


        @pytest.mark.parametrize(
            VIEW_REQUEST_PARAMS,
            [
                pytest.param(data_delete.get_empty_category_id_delete(), id='empty_category_id')
            ],
            indirect=[VIEW_REQUEST_PARAMS]
        )
        def test__empty_category_id(self, view_request_params: ParamViewRequestType):
            # GIVEN
            params = view_request_params
            client, path, username, delete_body, expected = (params.client, params.path, params.login_username, params.delete_body,  params.expected_response)
            # WHEN
            client.login(username=username)
            actual = client.delete(path, delete_body)
            # THEN
            assert actual.status_code == HTTP_422_UNPROCESSABLE_ENTITY
            assert actual.data == expected