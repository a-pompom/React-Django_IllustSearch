import * as BaseData from 'Common/BaseData';
import Cookies from 'js-cookie';

/**
 * APIからリソースを取得
 * 
 * @param {string} url リソース取得先URL
 * 
 * @return {Promise} responseJSON レスポンスをJSONに整形するPromiseオブジェクト
 */
export const get = async <Response>(url: string): Promise<Response> => {

    // クッキーを利用可能とし、APIを利用できるようCORSでリクエストを送信
    const requestOption: RequestInit = {
        method: 'get',
        credentials: 'include',
        mode: 'cors',
    }

    const response = await fetch(url, requestOption);
    const responseJSON = await response.json();
    return {
        ...responseJSON,
        ok: response.ok,
        status: response.status,
    };
};

/**
 * APIへPOSTリクエストを送信
 * 
 * @param url POSTリクエスト送信先URL
 * @param  body 送信するリクエストボディ
 * 
 * @return reponseJSON レスポンスをJSONに整形するPromiseオブジェクト
 */
export const post = async <Body, Response extends BaseData.BaseAPIResponse>(url: string, body: Body): Promise<Response> => {

    const requestOption: RequestInit = {
        method: 'POST',
        body: JSON.stringify(body),
        headers: new Headers(
            {
                'Accept': 'application/json',
                'content-type': 'application/json',
                'X-CSRFToken': Cookies.get('csrftoken'),
            }
        ),
        credentials: 'include',
        mode: 'cors',
    };

    const response = await fetch(url, requestOption)
    const responseJSON = await response.json();

    return {
        ...responseJSON,
        ok: response.ok,
        status: response.status,
    };
};