import * as IllustData from './illustListData';

/**
 * ActionをもとにStateを更新
 * 
 * @param state 更新対象のState
 * @param action イベントを格納したAction
 */
export const reducer = (state: IllustData.State, action: IllustData.IAction): IllustData.State => {

    // 初回描画
    if (action.type === 'ILLUST_LIST_GET') {

        state.illust_list = action.payload.response.body.illust_list;

        return state;
    }

    return state;
};