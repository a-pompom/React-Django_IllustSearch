import { Field } from 'Common/Field';
import * as BaseData from 'Common/BaseData';

// POSTリクエストボディ
export type PostBody = {
    username: string
};

// State要素・イベントハンドラ

export type FieldName = 'username';
// ユーザ登録処理のフィールドの値型
export type Value = string;
// ユーザ名フィールド
export type UsernameField<UsernameFieldName extends FieldName, UsernameValue extends Value> = Field<UsernameFieldName, UsernameValue>

// ユーザ名変更イベント
export type ChangeUsernameEvent = {(event: React.ChangeEvent<HTMLInputElement>): void}
// ユーザ登録イベント
export type CreateUserEvent = {(event: React.MouseEvent<HTMLButtonElement>): void}
// 表示切り替えイベント
export type ChangeViewEvent = {(event: React.MouseEvent<HTMLElement>)}

// 画面で管理する状態
export type State = BaseData.BaseState & {
    username: UsernameField<'username', string>
}

// Hook 状態・イベントハンドラを管理
export type Hook = {
    state: State,
    
    changeUsernameEvent: ChangeUsernameEvent,
    createUserEvent: CreateUserEvent,
    changeViewEvent: ChangeViewEvent,
}

// アクションインタフェース
export type IAction =  BaseData.IBaseAction;


// Component
// 入力Form Component
export type FormProps = {
    username: UsernameField<'username', string>,

    changeUsernameEvent: ChangeUsernameEvent,
    createUserEvent: CreateUserEvent,
}