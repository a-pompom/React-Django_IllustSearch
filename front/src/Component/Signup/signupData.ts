import { Field } from 'Common/Field';
import * as BaseData from 'Common/BaseData';

// 画面で表示する登録用ユーザ情報
export interface User {
    username: string
}

// POSTリクエストボディ
export interface PostBody {
    username: string
}

// State要素・イベントハンドラ

export type FieldNameUser = 'username';
// ユーザ登録処理のフィールドの値型
export type SignupValue = string;
// ユーザ名フィールド
export type UsernameField<FieldType, FieldName extends FieldNameUser> = Field<FieldType, FieldName>

// ユーザ名変更イベント
export type ChangeUsernameEvent = {(event: React.ChangeEvent<HTMLInputElement>): void}
// ユーザ登録イベント
export type CreateUserEvent = {(event: React.MouseEvent<HTMLButtonElement>): void}
// 表示切り替えイベント
export type ChangeViewEvent = {(event: React.MouseEvent<HTMLElement>)}

// 画面で管理する状態
export interface State extends BaseData.BaseState{
    username: UsernameField<string, 'username'>,
}

// Hook 状態・イベントハンドラを管理
export interface Hook {
    state: State,
    
    changeUsernameEvent: ChangeUsernameEvent,
    changeViewEvent: ChangeViewEvent,
    createUserEvent: CreateUserEvent,
}

// ユーザ名変更アクション
export interface UsernameChangeAction extends BaseData.BaseAction<'CHANGE_USER'> {
    type: 'CHANGE_USER',
    paylodad: {
        username: string
    }
}

// ユーザ名重複アクション
export interface UserDuplicateAction extends BaseData.BaseAction<'DUPLICATE_USER'> {
    type: 'DUPLICATE_USER',
    payload: {
        errorMessage: string
    }

}

// アクションインタフェース
export type IAction =  BaseData.IBaseAction | UsernameChangeAction | UserDuplicateAction;


// Component
// 入力Form Component
export interface FormProps {
    username: UsernameField<string, 'username'>,

    changeUsernameEvent: ChangeUsernameEvent,
    createUserEvent: CreateUserEvent,
}