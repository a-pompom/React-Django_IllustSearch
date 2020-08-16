import React from 'react';
import { useSignup } from'./useSignup';
import * as SignupData from './signupData';
import { Form } from './ViewComponent';

/**
 * ユーザ登録View
 * 
 * @param hook - 状態。イベントハンドラを格納
 */
export const SignupView: React.FC<SignupData.Hook> = ({
    state,
    changeUsernameEvent,
    createUserEvent,
    changeViewEvent,
}) => {

    return (
        <div className="Login">
	
            <header className="Header">
                
                <h2>Illust Search</h2>
                
            </header>

            {/* ユーザ情報入力フォーム */}
            <Form 
                username={state.username}

                changeUsernameEvent={changeUsernameEvent}
                createUserEvent={createUserEvent}
            />

            <button
                type="button"
                className="Cancel"

                onClick={changeViewEvent}
            >
                キャンセル
            </button>
	</div>
    );
};

/**
 * ユーザ登録コンポーネント
 * 
 */
export const Signup = () => {

    const hook = useSignup();

    return (
        <SignupView {...hook} />
    );
};