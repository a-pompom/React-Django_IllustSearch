from django.urls import path

from .views import LoginView, SignUpView, UserValidateUniqueView, AuthenticationView

app_name = 'login'

urlpatterns = [
        # ログイン
        path('', LoginView.as_view(), name='login'),
        # ユーザ登録
        path('signup/', SignUpView.as_view(), name='signup'),
        # ユーザ重複チェック
        path('validate/user/', UserValidateUniqueView.as_view(), name='user_validate'),
        # 認証
        path('auth_check/', AuthenticationView.as_view(), name='auth_check'),
]