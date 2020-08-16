import * as H from 'history';

import * as BaseData from 'Common/BaseData';
import { Setting } from 'settings';

import * as SignupData from './signupData';

/**
 * ユーザ名重複時処理 Stateのユーザ名フィールドへエラーメッセージを格納するアクションを発火
 * 
 * @param response 処理結果 エラーメッセージを格納
 * @param dispatch Actionを発火させるためのdispatch関数
 */
export const handleValidateUniqueUserFailure = (
    response: BaseData.PostResponse,
    fieldName: SignupData.FieldName,
    dispatch: React.Dispatch<SignupData.IAction>
) => {

    const action: BaseData.AfterValidationAction<SignupData.FieldName, SignupData.Value> = {
        type: 'AFTER_VALIDATION',
        payload: {
            results: [{
                isValid: false,
                fieldName,
                fieldValue: null,
                errors: [response.errors[0].message] // 今回はユーザ名のみ利用するので、決め打ち
            }]
        }
    };

    dispatch(action);
};

/**
 * ユーザ登録成功ハンドラ ログイン画面へ遷移
 * 
 * @param response 処理結果
 * @param history View変更用のHistoryAPI
 */
export const handleSuccessUserCreate = (
    response: BaseData.PostResponse,
    history: H.History<{}>
) => {
    history.push(Setting.VIEW_PATH.LOGIN);
}