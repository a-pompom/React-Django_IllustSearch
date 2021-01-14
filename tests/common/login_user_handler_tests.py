import pytest
from rest_framework import status
from common.login_user_handler import login_user_handler, LoginRequiredMixin

from .login_user_handler_data import data_get_login_user, data_get_initial
from common.exception_handler import UnAuthorizedException

class TestLoginUserHandler:

    class Test__get_login_user:

        def test__specified_user_request(self):
            # GIVEN
            sut = login_user_handler
            request, expected = data_get_login_user.get_specified_user_request()
            # WHEN
            actual = sut.get_login_user(request)
            # THEN
            assert actual == expected

        def test__anonymous_user_request(self):
            # GIVEN
            sut = login_user_handler
            request, expected = data_get_login_user.get_anonymous_user_request()
            # WHEN
            actual = sut.get_login_user(request)
            # THEN
            assert actual is expected

    class Test__initial:

        def test__specified_user_request(self):
            # GIVEN
            view, request = data_get_initial.get_specified_user_request()
            # WHEN
            actual = view.initial(request)
            # THEN
            assert actual is None

        def test__anonymous_user_request(self):
            # GIVEN
            view, request = data_get_initial.get_anonymous_user_request()
            # THEN
            with pytest.raises(UnAuthorizedException):
                # WHEN
                view.initial(request)