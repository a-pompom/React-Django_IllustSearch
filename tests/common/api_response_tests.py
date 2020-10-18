from common.api_response import *

from .api_response_data import data_render_success_response, data_render_to_error_response, data_render_to_failure_response

class TestAPIResponse:

    class TestRenderToSuccessResponse:
        """ 成功APIレスポンス """

        def test_メッセージのみを受け取るとbodyへメッセージが格納されたレスポンスが得られること(self):

            # GIVEN
            sut = APIResponseMixin()
            message, body, expected = data_render_success_response.get_only_message()

            # WHEN
            actual = sut.render_to_success_response(message)

            # THEN
            assert actual == expected

        def test_bodyを受け取るとbodyをディクショナリへ格納したレスポンスが得られること(self):

            # GIVEN
            sut = APIResponseMixin()
            message, body, expected = data_render_success_response.get_response_with_body()

            # WHEN
            actual = sut.render_to_success_response(body=body)

            # THEN
            assert actual == expected

    class TestRenderToErrorResponse:

        def test_単一のフィールドエラーが得られること(self):
            # GIVEN
            sut = APIResponseMixin()
            message, errors, expected = data_render_to_error_response.get_single_field_error()

            # WHEN
            actual = sut.render_to_error_response(message, errors)

            # THEN
            assert actual == expected

        def test_複数メッセージがカンマ区切りで結合されること(self):
            # GIVEN
            sut = APIResponseMixin()
            message, errors, expected = data_render_to_error_response.get_comma_separated_field_error()

            # WHEN
            actual = sut.render_to_error_response(message, errors)

            # THEN
            assert actual == expected

        def test_複数フィールドの複数メッセージを格納したレスポンスが取得できること(self):
            # GIVEN
            sut = APIResponseMixin()
            message, errors, expected = data_render_to_error_response.get_multiple_field_error()

            # WHEN
            actual = sut.render_to_error_response(message, errors)

            # THEN
            assert actual == expected

    class TestRenderToFailureResponse:
        
        def test_失敗メッセージがbodyへ格納されること(self):

            # GIVEN
            sut = APIResponseMixin()
            message, expected = data_render_to_failure_response.get_failure()

            # WHEN
            actual = sut.render_to_failure_response(message)

            # THEN
            assert actual == expected