import React from 'react';

import { Setting } from 'settings';
import * as BaseData from 'Common/BaseData';

import { LoginRequired } from 'Component/Auth/ViewLoginRequiredRoute';

import { getAPIInfo } from '../testUtils/testAPIUtils';
import { render } from 'react-dom';

/**
 * 認証フックで利用するテストデータを取得
 */
const getAuthHookData = () => {

    // 認証成功APIレスポンス
    const successAPI = getAPIInfo<null, BaseData.BaseAPIResponse>(
        `${Setting.API_ENDPOINT}${Setting.API_PATH.AUTH.AUTH_CHECK}`,
        'get',
        {body: {message: 'OK'}, ok: true, status: 200},
        null,
    );
    // 認証失敗APIレスポンス
    const failureAPI = getAPIInfo<null, BaseData.BaseAPIResponse>(
        `${Setting.API_ENDPOINT}${Setting.API_PATH.AUTH.AUTH_CHECK}`,
        'get',
        {body: {message: 'unauthorized...'}, ok: false, status: 401},
        null,
    );

    /**
     * 初回描画イベント
     * 
     * @param container コンポーネント描画対象Div要素
     */
    const initEvent = (container: HTMLDivElement) => {
    
        return () => {
            render(
                <LoginRequired><div></div></LoginRequired>
                , container
            );
        };
    };

    return {
        successAPI,
        failureAPI,
        initEvent,
    };
};

export const dataAuthHook = getAuthHookData();