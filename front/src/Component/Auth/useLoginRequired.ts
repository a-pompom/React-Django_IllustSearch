import { useEffect, useState } from 'react';
import { useHistory } from 'react-router-dom';

import { get } from 'Common/Logic/apiHandler';
import { Setting } from 'settings';

import * as AuthData from './authData';
import { Phase } from 'Common/Phase';

/**
 * 認証フック
 * 
 * @returns 認証処理の進行状況を表すState
 */
export const useLoginRequired = (): AuthData.Hook => {

    const [state, setState] = useState<AuthData.State>({phase: new Phase('LOADING')});
    const history = useHistory();

    // 認証処理
    useEffect(() => {

        const emitGet = async () => {

            const response = await get(Setting.API_PATH.AUTH.AUTH_CHECK);

            // 認証失敗
            if (response.status === 401) {
                history.replace(Setting.VIEW_PATH.LOGIN);
                return;
            }

            setState({phase: new Phase('IDLE')});
        };
        emitGet();
    }, []);

    return {
        state: state
    };
};