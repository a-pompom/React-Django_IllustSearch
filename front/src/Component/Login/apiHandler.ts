import * as H from 'history';

import * as BaseData from 'Common/BaseData';
import * as FetchUtil from 'Common/FetchUtil';
import { PostResponse } from 'Common/BaseData';
import { Setting } from 'settings';

import * as LoginData from './loginData';

// APIパス
const END_POINT = Setting.API_ENDPOINT;
const LOGIN_PATH = Setting.API_PATH.LOGIN;

/**
 * APIよりカテゴリの一覧を取得
 */
export const getUserList = async <GetParameter>(param?: GetParameter): Promise<LoginData.User[]> => {

    const response = await FetchUtil.get<LoginData.UserResponse>(`${END_POINT}/${LOGIN_PATH}`);

    // レスポンス→View用オブジェクトへ詰め替え
    const userList = response.users.map((user): LoginData.User => {

        return {
            username: user.username,
            iconPath: ''
        };
    });

    return userList;
};

/**
 * ログインAPIでログイン処理を実行
 * 
 * @param body - ログインユーザ名を格納したリクエストボディ
 * 
 * @returns response 処理結果メッセージとステータスコードを格納したレスポンス
 */
export const postLogin = async <Body>(body: Body): Promise<PostResponse> => {

    const response = await FetchUtil.post<Body, PostResponse>(`${END_POINT}/${LOGIN_PATH}`, body);

    return response;
}

/**
 * ログイン成功処理 TOP画面へ遷移
 * 
 * @param history 画面遷移用のHistoryAPI
 */
export const handlePostSuccess = (history: H.History<{}>) => {

    history.push(Setting.VIEW_PATH.SIGNUP);
}

/**
 * ログイン失敗処理 エラーメッセージを表示
 * 
 * @param dispatch アクションの実行 エラーメッセージを一定時間表示後に消去するために利用
 */
export const handlePostFailure = (
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