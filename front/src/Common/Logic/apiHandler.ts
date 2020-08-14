import * as BaseData from 'Common/BaseData';
import * as FetchUtil from 'Common/FetchUtil';
import { Setting } from 'settings';

// APIパス
const END_POINT = Setting.API_ENDPOINT;

/**
 * ボディを特定のエンドポイントへ送信するシンプルなPOSTリクエストを発行
 * 
 * @param apiPath POSTリクエスト送信先
 * @param body POSTリクエストボディ
 */
export const post = async <Body>(body: Body, apiPath: string): Promise<BaseData.PostResponse> => {

    const response = await FetchUtil.post<Body, BaseData.PostResponse>(`${END_POINT}${apiPath}`, body);

    return response;
}