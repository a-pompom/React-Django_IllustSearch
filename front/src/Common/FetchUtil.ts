import * as BaseData from 'Common/BaseData';

/**
 * APIからリソースを取得
 * 
 * @param {string} url リソース取得先URL
 * 
 * @return {Promise} responseJSON レスポンスをJSONに整形するPromiseオブジェクト
 */
export const get = async <Response>(url: string): Promise<Response> => {

    const response = await fetch(url)
        .then(async (res) => {
            const resJSON = await res.json();
            return {
                ...resJSON,
                ok: res.ok
            }
        });

    return response;
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

    const options = {
        method: 'POST',
        body: JSON.stringify(body),
        headers: new Headers({'Accept': 'application/json','content-type': 'application/json'})
    };

    const response = await fetch(url, options)
        .then(async (res) => {
            const resJSON = await res.json();
            return {
                ...resJSON,
                ok: res.ok
            }
        });

    return response;
};