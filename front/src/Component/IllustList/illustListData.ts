import * as BaseData from 'Common/BaseData';

export type Illust = {
    path: string;
};

// APIからのレスポンス
export type GetResponse = BaseData.BaseAPIResponse & {
    body: BaseData.BaseAPIResponse['body'] & {
        illust_list: Illust[]
    };
};


// 画面で管理する状態
export type State = BaseData.BaseState & {
    illust_list: Illust[]
};

// Hook 状態・イベントハンドラを管理
export type Hook = {
    state: State,
};

// 初期描画アクション
export type IllustListGetAction = BaseData.BaseAction<'ILLUST_LIST_GET'> & {
    payload: {
        response: GetResponse
    }
};

// アクションインタフェース
export type IAction = BaseData.IBaseAction | IllustListGetAction;

// Action Creator
export const illustListGet = (response: GetResponse): IllustListGetAction => {
    return {
        type: 'ILLUST_LIST_GET',
        payload: {
            response
        }
    };
};