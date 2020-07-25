export interface User {
    username: string,
    iconPath: string
}

export interface UserResponse {
    users: {username: string}[]
}

// 画面で管理する状態
export interface LoginState {
    users: User[],
    loginUsername: string
}

// 状態・イベントハンドラを管理
export interface LoginHook {
    state: LoginState
};