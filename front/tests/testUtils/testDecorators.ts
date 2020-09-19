import FetchMock, { mock } from 'fetch-mock';
import { configure } from "enzyme/build";
import Adapter from "enzyme-adapter-react-16/build";

/**
 * コンポーネントの描画にDOM操作が必要なテスト
 * 
 * @param testName 処理テスト名
 * @param testBody テスト処理本体
 * @param isInNest? 他のテスト内で呼ばれるか テスト関数はネストして呼び出せないので、呼び出しを制御するために利用
 */
export const domTest = (testName: string, testBody: (container: HTMLDivElement, ...args: any)=> void, isInNest?: boolean) => {

    /**
     * テスト処理本体をデコレートする関数
     * コンポーネント描画用のdiv要素をテスト前に生成し、テスト後に破棄
     */
    const testFunction = () => {

        // Setup コンポーネントを配置するためのdiv要素をbody配下へ追加
        const body = document.querySelector('body');
        const container = document.createElement('div');

        container.setAttribute('id', 'Container');
        body.appendChild(container);

        // テスト処理
        testBody(container);

        // Teardown
        // 作成したdiv要素をクリア
        body.removeChild(container);
    }

    // 他のテストデコレータと併用する場合は、ネストできないので、test関数は実行しない
    if (isInNest) {
        testFunction();
        return;
    }

    test(testName, testFunction);
};

/**
 * コンポーネントの描画にDOM操作が必要なテスト 非同期処理を挟む用
 * 
 * @param testName 処理テスト名
 * @param testBody テスト処理本体
 * @param isInNest? 他のテスト内で呼ばれるか テスト関数はネストして呼び出せないので、呼び出しを制御するために利用
 */
export const asyncDomTest = (testName: string, testBody: (container: HTMLDivElement, ...args: any)=> Promise<any>, isInNest?: boolean) => {

    /**
     * テスト処理本体をデコレートする関数
     * コンポーネント描画用のdiv要素をテスト前に生成し、テスト後に破棄
     */
    const testFunction = async () => {

        // Setup コンポーネントを配置するためのdiv要素をbody配下へ追加
        const body = document.querySelector('body');
        const container = document.createElement('div');

        container.setAttribute('id', 'Container');
        body.appendChild(container);

        // テスト処理
        await testBody(container);

        // Teardown
        // 作成したdiv要素をクリア
        body.removeChild(container);
    }

    // 他のテストデコレータと併用する場合は、ネストできないので、test関数は実行しない
    if (isInNest) {
        testFunction();
        return;
    }

    test(testName, testFunction);
};


/**
 * コンポーネントの描画にDOM操作が必要なテスト 複数テストをまとめて実行
 * 
 * @param testArgs<Args> 各テストで扱うパラメータの配列をまとめた配列
 * @param testName 全体のテスト処理名
 * @param testBody テスト処理本体 処理ごとにArgsの各要素を引数に持つ
 */
export const domTestEach = <Args extends any[]>(
    testArgs: Args[], 
    testName: string, 
    testBody: (container: HTMLDivElement, ...args: Args)=> void) => {
    
    const testFunction = (...args: Args) => {

        // Setup コンポーネントを配置するためのdiv要素をbody配下へ追加
        const container = document.createElement('div');
        container.setAttribute('id', 'Container');
        document.body.appendChild(container);

        // テスト処理本体
        testBody(container, ...args);

        // Teardown
        // 作成したdiv要素をクリア
        document.body.removeChild(container);
    };

    test.each(testArgs)(testName, testFunction);
};

// APIモックを生成するためのオブジェクト情報
export type APIMockInfo<Response, Body> = {
    PATH: string,
    method: 'get' | 'post',
    expectedResponse: Response,
    body?: Body
};
/**
 * APIとの通信が必要なテスト
 * 
 * @param testName 実行テスト名
 * @param testBody テスト本体
 * @param apiMockInfoList APIのパス・メソッド・仮のレスポンスを格納したオブジェクト
 * @param isInNest? ネストしたテスト内か テストはネストして呼べないので、呼び出しを制御するために利用
 */
export const apiTest = async (
    testName: string, testBody: Function, apiMockInfoList: APIMockInfo<any, any>[], isInNest?: Boolean
) => {

    /**
     * テスト処理本体をデコレートする関数
     * 各APIのエンドポイントへのアクセスに対するレスポンスをモック化
     */
    const testFunction = async () => {

        // Setup
        // Reactのバージョンを固定
        configure({ adapter: new Adapter() });
        FetchMock.config.overwriteRoutes = false;

        // 各通信のレスポンスを固定
        apiMockInfoList.forEach(apiMockInfo => {

            const mockObject = {
                url: apiMockInfo.PATH, 
                method: apiMockInfo.method, 
            };
            if (mockObject.method === 'get') {
                mockObject['query'] = apiMockInfo.body;
            }
            if (mockObject.method === 'post') {
                mockObject['body'] = apiMockInfo.body;
            }

            FetchMock.mock(mockObject, () => ({body: apiMockInfo.expectedResponse, status: apiMockInfo.expectedResponse['status']}) );
        });

        // APIの発行は通常カスタムフックで実行されるため、検証にはコンポーネントのレンダリングが伴う
        // レンダリングは非同期で実行されるので、awaitで待機しなければ、モックAPIが呼ばれる前にモックがリセットされてしまう
        await testBody();

        // Teardown
        // モックのリセット
        FetchMock.reset();
    }

    if (isInNest) {
        await testFunction();
        return;
    }

    test(testName, testFunction);
}