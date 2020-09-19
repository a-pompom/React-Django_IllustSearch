import * as H from 'history';

import * as BaseData from 'Common/BaseData';
import { Setting } from 'settings';

import * as LoginData from './loginData';

/**
 * ログイン用ユーザ取得 画面表示用にStateを更新
 * 
 * @param response GETAPIレスポンス ユーザ情報を格納
 * @param dispatch State更新用のreducerを呼び出すためのdispatch関数
 */
export const handleUserGetSuccess = (response: LoginData.GetResponse, dispatch: React.Dispatch<LoginData.IAction>) => {

    const action: LoginData.UserGetAction = {
        type: 'USER_GET',
        payload: {
            response: response
        }
    };
    dispatch(action);
};

/**
 * ログイン成功処理 TOP画面へ遷移
 * 
 * @param response POST処理結果レスポンス
 * @param history 画面遷移用のHistoryAPI
 */
export const handlePostSuccess = (
    response: BaseData.BaseAPIResponse,
    history: H.History<{}>
) => {

    history.push(Setting.VIEW_PATH.TOP);
}

/**
 * ログイン失敗処理 エラーメッセージを表示
 * 
 * @param response POST処理結果レスポンス
 * @param dispatch アクションの実行 エラーメッセージを一定時間表示後に消去するために利用
 */
export const handlePostFailure = (
    response: BaseData.BaseAPIResponse,
    dispatch: React.Dispatch<BaseData.IBaseAction>, 
) => {
    const timer = global.setTimeout(() => {

        const action: BaseData.IdleAction = {
            type: 'IDLE'
        };
        dispatch(action);

    // CSSにあわせ、メッセージが視認できる程度の時間経過後に初期化
    }, 1800);

    const action: BaseData.AddTimerAction = {
        type: 'ADD_TIMER',
        payload: {
            timer
        }
    };
    dispatch(action);
}