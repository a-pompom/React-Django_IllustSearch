import * as LoginData from './loginData';
import * as BaseData from 'Common/BaseData';
import { Message } from 'message.properties';

// ユーザ名変更アクション
export interface UsernameChangeAction extends BaseData.BaseAction<'CHANGE_USER'> {
    type: 'CHANGE_USER',
    paylodad: {
        username: string
    }
}
// 初期描画アクション
export interface FetchSuccessAction extends BaseData.BaseAction<'FETCH_SUCCESS'> {
    payload: {
        response: LoginData.GetResponse
    }
};

// アクションインタフェース
export type IAction = BaseData.IBaseAction | FetchSuccessAction | UsernameChangeAction;

/**
 * Stateを更新
 * 
 * @param state - 画面の表示・入力情報を格納したState
 * @param action - 初期描画/ユーザ名変更アクション
 * 
 * @returns state 更新後のStateオブジェクト 
 */
export const reducer = (state: LoginData.State, action: IAction): LoginData.State => {

    // 初期描画 APIから取得したユーザをログイン一覧ユーザへ設定
    if (action.type === 'FETCH_SUCCESS'){

        state.users = action.payload.response.users;

        return state;
    }

    // ユーザ名変更 ログインユーザ名をStateへ格納
    if (action.type === 'CHANGE_USER') {

        state.loginUsername.value = action.paylodad.username;

        return state;
    }

    // POST失敗 ログイン失敗メッセージを設定
    if (action.type === 'FAILURE_POST') {
        state.phase.message = Message.Login.Failure;

        return state;
    }
    return state;
};