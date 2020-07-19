export class FetchUtil {

    /**
     * APIからリソースを取得
     * 
     * @param {string} url リソース取得先URL
     * 
     * @return {Promise} responseJSON レスポンスをJSONに整形するPromiseオブジェクト
     */
    static async get<T>(url: string): Promise<T> {

        let responseJSON: Promise<T>;
        try {
            const response = await fetch(url);
            responseJSON = await response.json() as Promise<T>;

        } catch(response) {
            responseJSON = await response.json() as Promise<T>;
        }

        return responseJSON;
    }

    /**
     * APIへPOSTリクエストを送信
     * 
     * @param {string} url POSTリクエスト送信先URL
     * @param {Object} body 送信するリクエストボディ
     * 
     * @return {Promise} reponseJSON レスポンスをJSONに整形するPromiseオブジェクト
     */
    static async post<Body, Response>(url: string, body: Body): Promise<Response> {

        const options = {
            method: 'POST',
            body: JSON.stringify(body),
            headers: new Headers({'Accept': 'application/json','content-type': 'application/json'})
        };

        let responseJSON: Promise<Response>;
        try {
            const response = await fetch(url, options);
            responseJSON = await response.json() as Promise<Response>;

        } catch(response) {
            responseJSON = await response.json() as Promise<Response>;
        }

        return responseJSON;
    }
}