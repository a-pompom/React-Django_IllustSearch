export const Setting = {
    // アプリのAPIエンドポイント
    API_ENDPOINT: 'http://localhost:8000/api/v1/',

    // 各APIへのパス
    API_PATH: {
        AUTH: {
            LOGIN: 'login/',
            SIGNUP: 'login/signup/',
            AUTH_CHECK: 'login/auth_check/',
            VALIDATE_UNIQUE_USER: 'login/validate/user',
        },
        ILLUST: {
            LIST: 'illust/illust_list/',
        }
    },

    // 画面コンポーネントへのパス
    VIEW_PATH: {
        LOGIN: '/',
        SIGNUP: '/signup/',
        TOP: '/image/list',
    },
}