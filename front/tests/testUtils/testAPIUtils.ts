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