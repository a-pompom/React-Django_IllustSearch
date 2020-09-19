import * as BaseData from 'Common/BaseData';
import { APIMockInfo } from './testDecorators';

export  const getAPIInfo = <Body, APIResponse extends BaseData.BaseAPIResponse>(path: string, method: 'get' | 'post', response: APIResponse, body: Body) => {
    const apiInfo: APIMockInfo<APIResponse, Body> = {
        PATH: path,
        method: method,
        expectedResponse: response,
        body: body
    } 
    return apiInfo
};

/**
 * ベースとなる正常系レスポンスを取得
 * 
 * @return OKレスポンス
 */
export const getSimpleOkResponse = (): BaseData.BaseAPIResponse => {

    return {
        body: {
            message: 'ok'
        },
        status: 200,
        ok: true
    };
};