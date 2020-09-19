export const Setting = {
    // アプリのAPIエンドポイント
    API_ENDPOINT: 'http://localhost:8000/api/v1/',

    // 各APIへのパス
    API_PATH: {
        LOGIN: 'login/',
        SIGNUP: 'login/signup/',
        VALIDATE_UNIQUE_USER: 'login/validate/user',
    },

    // 画面コンポーネントへのパス
    VIEW_PATH: {
        LOGIN: '/',
        SIGNUP: '/signup/',
        TOP: '/image/list',
    },
}