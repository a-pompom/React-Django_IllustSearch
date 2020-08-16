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

export type FieldName = 'username';
// ユーザ登録処理のフィールドの値型
export type Value = string;
// ユーザ名フィールド
export type UsernameField<UsernameValue extends Value, UsernameFieldName extends FieldName> = Field<UsernameValue, UsernameFieldName>

// ユーザ名変更イベント
export type ChangeUsernameEvent = {(event: React.ChangeEvent<HTMLInputElement>): void}
// ユーザ登録イベント
export type CreateUserEvent = {(event: React.MouseEvent<HTMLButtonElement>): void}
// 表示切り替えイベント
export type ChangeViewEvent = {(event: React.MouseEvent<HTMLElement>)}

// 画面で管理する状態
export interface State extends BaseData.BaseState {
    username: UsernameField<string, 'username'>
}

// Hook 状態・イベントハンドラを管理
export interface Hook {
    state: State,
    
    changeUsernameEvent: ChangeUsernameEvent,
    createUserEvent: CreateUserEvent,
    changeViewEvent: ChangeViewEvent,
}

// アクションインタフェース
export type IAction =  BaseData.IBaseAction;


// Component
// 入力Form Component
export interface FormProps {
    username: UsernameField<string, 'username'>,

    changeUsernameEvent: ChangeUsernameEvent,
    createUserEvent: CreateUserEvent,
}