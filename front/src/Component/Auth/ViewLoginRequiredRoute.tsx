import React from 'react';

import { PhaseView } from 'Common/Views/ViewPhase';

import { useLoginRequired } from'./useLoginRequired';
import * as AuthData from './authData';

type Prop = AuthData.Hook & {
    children: React.ReactChild
};

/**
 * 認証View
 * 
 * @param hook - 状態を格納
 */
export const LoginRequiredView: React.FC<Prop> = ({
    state,
    children,
}) => {

    return (
        <React.Fragment>
            {state.phase.currentPhase === 'IDLE' ? 
                children :

                <PhaseView
                    phase={state.phase.currentPhase}
                    message={state.phase.message}
                />
            }
        </React.Fragment>
    );
};

/**
 * 認証コンポーネント
 * 
 * @remarks
 *     認証APIを通じて、アクセスしたユーザがログイン済みか判定
 */
export const LoginRequired = ({children}: {children: React.ReactChild}) => {

    const loginRequiredHook = useLoginRequired();

    return (
        <LoginRequiredView {...loginRequiredHook} children={children} />
    );
};