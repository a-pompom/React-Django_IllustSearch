import * as BaseData from 'Common/BaseData';
import * as FetchUtil from 'Common/FetchUtil';
import { Setting } from 'settings';

// APIパス
const END_POINT = Setting.API_ENDPOINT;

/**
 * クエリパラメータオブジェクトを「?param1=value&param2=value2」の形へ整形
 * 
 * @param param クエリパラメータオブジェクト
 */
export const getQueryString = <Param>(param: Param): string => {

    // クエリが空の場合は何もしない
    if (! param) {
        return '';
    }

    let query = '?';

    for (let key in param) {
        query += `${key}=${param[key]}`;
        query += '&';
    }

    return query.substring(0, query.length-1);
}

/**
 * GETリクエストを発行
 * 
 * @param apiPath GETリクエスト送信先
 * @param param クエリ文字列オブジェクト
 */
export const get = async<Response extends BaseData.BaseAPIResponse, Param={}>(
    apiPath: string,
    param?: Param
): Promise<Response> => {

    const queryString = getQueryString(param);
    const response = await FetchUtil.get<Response>(`${END_POINT}${apiPath}${queryString}`);

    return response;
}

/**
 * POSTリクエストを発行
 * 
 * @param apiPath POSTリクエスト送信先
 * @param body POSTリクエストボディ
 */
export const post = async <Body, Response extends BaseData.BaseAPIResponse>(
    apiPath: string,
    body: Body
): Promise<Response> => {

    const response = await FetchUtil.post<Body, Response>(`${END_POINT}${apiPath}`, body);

    return response;
}