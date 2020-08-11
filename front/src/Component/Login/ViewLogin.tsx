import React from 'react';

import { PhaseView } from 'Common/ViewPhase';

import { useLogin } from'./useLogin';
import * as LoginData from './loginData';
import { UserList, Form } from './ViewComponent';

/**
 * ログインView
 * 
 * @param hook - 状態。イベントハンドラを格納
 */
export const LoginView: React.FC<LoginData.Hook> = ({
    state,
    changeUsername,
    changeViewEvent,
    loginEvent,
}) => {

    return (
        <React.Fragment>
            <PhaseView
                phase={state.phase.currentPhase}
                message={state.phase.message}
            />

            <div className="Login">
        
                <header className="Header">
                    
                    <h2>Illust Search</h2>
                    
                </header>

                {/* ユーザ情報入力フォーム */}
                <Form 
                    loginUsername={state.loginUsername}

                    changeUsername={changeUsername}
                    loginEvent={loginEvent}
                />

                {/* ログインユーザ一覧 */}
                <UserList
                    users={state.users} 
                    changeViewEvent={changeViewEvent}
                />
            </div>
        </React.Fragment>
    );
};

/**
 * ログインコンポーネント
 * 
 * @remarks
 *     ログイン機能と、ユーザ作成・作成済みユーザによるログインを提供
 */
export const Login = () => {

    const loginHook = useLogin();

    return (
        <LoginView {...loginHook} />
    );
};