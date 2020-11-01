import React from 'react';
import * as IllustData from './illustListData';

/**
 * イラスト一覧取得成功時処理 reducerへ取得成功Actionを発行
 * 
 * @param response APIから得られたレスポンス
 * @param dispatch Actionをreducerへ伝播させるdispatcher
 */
export const handleIllustListGetSuccess = (
    response: IllustData.GetResponse,
    dispatch: React.Dispatch<IllustData.IAction>
): void => {

    dispatch(IllustData.illustListGet(response));
};