import * as LoginData from './loginData';
import { Message } from 'message.properties';

/**
 * Stateを更新
 * 
 * @param state - 画面の表示・入力情報を格納したState
 * @param action - 初期描画/ユーザ名変更アクション
 * 
 * @returns state 更新後のStateオブジェクト 
 */
export const reducer = (state: LoginData.State, action: LoginData.IAction): LoginData.State => {

    // 初期描画 APIから取得したユーザをログイン一覧ユーザへ設定
    if (action.type === 'USER_GET'){

        state.users = action.payload.response.body.users;

        return state;
    }

    // ユーザ名変更 ログインユーザ名をStateへ格納
    if (action.type === 'CHANGE_USER') {

        state.username.value = action.paylodad.username;

        return state;
    }

    // POST失敗 ログイン失敗メッセージを設定
    if (action.type === 'FAILURE_POST') {
        state.phase.message = Message.Login.Failure;

        return state;
    }
    return state;
};