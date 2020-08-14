import React from 'react';

import { Error } from 'Common/Views/ViewError';

import * as SignupData from './signupData';

/**
 * ユーザ登録画面Formコンポーネント
 * 
 */
export const Form: React.FC<SignupData.FormProps> = ({
    username,
    changeUsernameEvent,
    createUserEvent
}) => {

    return (
        <article className="Form">
            
            <form action="#" method="post">
                
                {/* ユーザ名 */}
                <input 
                    type="text"
                    id="username"
                    className="Input"

                    placeholder={username.label}
                    defaultValue={username.value}
                    onBlur={changeUsernameEvent}
                />
                {username.errors.length === 0 ? null : 
                    <Error errors={username.errors} />}

                {/* ユーザ登録ボタン */}
                <input
                    type="submit"
                    className="Button"

                    value="ユーザ登録"
                    onClick={createUserEvent}
                />

            </form>
        </article>
    );
}