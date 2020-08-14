import * as SignupData from './signupData';

/**
 * Stateを更新
 * 
 * @param state - 画面の入力情報を格納したState
 * @param action - イベントとパラメータを格納したアクション
 * 
 * @returns state 更新後のStateオブジェクト 
 */
export const reducer = (state: SignupData.State, action: SignupData.IAction): SignupData.State => {

    // ユーザ名変更 ユーザ名をStateへ格納
    if (action.type === 'CHANGE_USER') {

        state.username.errors = [];
        state.username.value = action.paylodad.username;
    }

    // ユーザ名重複 エラーメッセージをユーザ名フィールドへ追加
    if (action.type === 'DUPLICATE_USER') {

        state.username.errors.push(action.payload.errorMessage);
    }

    return state;
};