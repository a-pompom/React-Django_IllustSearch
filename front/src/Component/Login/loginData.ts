import { Field } from 'Common/Field';
import * as BaseData from 'Common/BaseData';

// 画面で表示するログイン用ユーザ情報
export interface User {
    username: string,
    iconPath: string
}
// APIからのレスポンス
export interface UserResponse {
    users: {username: string}[]
}
// POSTリクエストボディ
export interface PostBody {
    username: string
}

// State要素・イベントハンドラ

export type LoginFieldName = 'loginUsername';
// ログイン処理のフィールドの値型
export type LoginValue = string;
// ログインユーザ名フィールド
export type LoginUsername<FieldType, FieldName extends LoginFieldName> = Field<FieldType, FieldName>

// ユーザ名変更イベント
export type ChangeUsername = {(event: React.ChangeEvent<HTMLInputElement>): void}
// ログインイベント
export type LoginEvent = {(event: React.MouseEvent<HTMLButtonElement>): void}
// 表示切り替えイベント
export type ChangeViewEvent = {(event: React.MouseEvent<HTMLElement>)}

// 画面で管理する状態
export interface State extends BaseData.BaseState{
    users: User[],
    loginUsername: LoginUsername<string, 'loginUsername'>,
}

// Hook 状態・イベントハンドラを管理
export interface Hook {
    state: State,
    
    changeUsername: ChangeUsername,
    changeViewEvent: ChangeViewEvent,
    loginEvent: LoginEvent,
}

// Component
// 入力Form Component
export interface FormProps {
    loginUsername: LoginUsername<string, 'loginUsername'>,

    changeUsername: ChangeUsername,
    loginEvent: LoginEvent,
}
// ログインユーザ一覧 Component
export interface UserListProps {
    users: User[],

    changeViewEvent: ChangeViewEvent
}