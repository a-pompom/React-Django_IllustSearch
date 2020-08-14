import * as BaseData from 'Common/BaseData';
import * as FetchUtil from 'Common/FetchUtil';
import { PostResponse } from 'Common/BaseData';
import { Setting } from 'settings';

import * as SignupData from './signupData';

// APIパス
const END_POINT = Setting.API_ENDPOINT;
const LOGIN_PATH = Setting.API_PATH.LOGIN;

/**
 * ユーザ名重複時処理 Stateのユーザ名フィールドへエラーメッセージを格納するアクションを発火
 * 
 * @param response 処理結果 エラーメッセージを格納
 * @param dispatch Actionを発火させるためのdispatch関数
 */
export const handleValidateUniqueUserFailure = (
    response: BaseData.PostResponse,
    dispatch: React.Dispatch<SignupData.IAction>
) => {

    // 今回はユーザ名のみ利用するので、決め打ち
    const errorMessage = response.errors[0].message;

    const action: SignupData.UserDuplicateAction = {
        type: 'DUPLICATE_USER',
        payload: {
            errorMessage
        }
    };

    dispatch(action);
};

/**
 * ログインAPIでログイン処理を実行
 * 
 * @param body - ログインユーザ名を格納したリクエストボディ
 * 
 * @returns response 処理結果メッセージとステータスコードを格納したレスポンス
 */
export const postUserCreate = async <Body>(body: Body): Promise<PostResponse> => {

    const response = await FetchUtil.post<Body, PostResponse>(`${END_POINT}${LOGIN_PATH}`, body);

    return response;
}
