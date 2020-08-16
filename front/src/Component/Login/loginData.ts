import { Field } from 'Common/Field';
import * as BaseData from 'Common/BaseData';

// 画面で表示するログイン用ユーザ情報
export interface User {
    username: string,
    iconPath: string
}
// APIからのレスポンス
export interface GetResponse extends BaseData.BaseGetResponse {
    users: User[]
}
// POSTリクエストボディ
export interface PostBody {
    username: string
}

// State要素・イベントハンドラ

export type FieldName = 'username';
// ログイン処理のフィールドの値型
export type Value = string;
// ログインユーザ名フィールド
export type UsernameField<UsernameFieldName extends FieldName, UsernameValue extends Value> = Field<UsernameFieldName, UsernameValue>

// ユーザ名変更イベント
export type ChangeUsername = {(event: React.ChangeEvent<HTMLInputElement>): void}
// ログインイベント
export type LoginEvent = {(event: React.MouseEvent<HTMLButtonElement>): void}
// 表示切り替えイベント
export type ChangeViewEvent = {(event: React.MouseEvent<HTMLElement>)}

// 画面で管理する状態
export interface State extends BaseData.BaseState {
    username: UsernameField<'username', string>
    users: User[]
}

// Hook 状態・イベントハンドラを管理
export interface Hook {
    state: State,
    
    changeUsername: ChangeUsername,
    changeViewEvent: ChangeViewEvent,
    loginEvent: LoginEvent,
}

// ユーザ名変更アクション
export interface UsernameChangeAction extends BaseData.BaseAction<'CHANGE_USER'> {
    type: 'CHANGE_USER',
    paylodad: {
        username: string
    }
}
// 初期描画アクション
export interface FetchSuccessAction extends BaseData.BaseAction<'FETCH_SUCCESS'> {
    payload: {
        response: GetResponse
    }
};

// アクションインタフェース
export type IAction = BaseData.IBaseAction | FetchSuccessAction | UsernameChangeAction;

// Component
// 入力Form Component
export interface FormProps {
    username: UsernameField<'username', string>

    changeUsername: ChangeUsername,
    loginEvent: LoginEvent,
}
// ログインユーザ一覧 Component
export interface UserListProps {
    users: User[],

    changeViewEvent: ChangeViewEvent
}