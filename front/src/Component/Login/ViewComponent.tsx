import React from 'react';
import * as LoginData from './loginData';

/**
 * ログイン画面Formコンポーネント
 * 
 * @remarks
 *     画面の入力値をログインユーザ名として保持し、ボタンクリックでログイン
 */
export const Form: React.FC<LoginData.FormProps> = ({
    loginUsername,
    changeUsername,
    loginEvent,
}) => {

    return (
        <article className="Form">
            
            <form action="#" method="post">
                
                {/* ユーザ名 */}
                <input 
                    type="text"
                    id="username"
                    className="Input"

                    name={loginUsername.name}
                    placeholder={loginUsername.label}
                    defaultValue={loginUsername.value}
                    onBlur={changeUsername}
                />

                <input
                    type="submit"
                    className="Button"
                    value="ログイン"

                    onClick={loginEvent}
                />
            </form>
        </article>
    );
};

/**
 * ログイン用ユーザ一覧コンポーネント
 * 
 * @remarks ログインユーザを一覧表示し、「+」ボタンクリックでログインとユーザ登録を切り替える
 */
export const UserList: React.FC<LoginData.UserListProps> = ({
    users,
    changeViewEvent
}) => {

    return (
        <ul className="Users">

            {/* ユーザ一覧 */}
            {users.map((user) => {
                return (
                    <li key={user.username} className="User">
                        { user.username }
                    </li>
                );
            })}

            {/* ログイン/ユーザ登録表示切り替え */}
            <li 
                onClick={changeViewEvent}
                className="Add"
            >
                +
            </li>
        </ul>
    );
};