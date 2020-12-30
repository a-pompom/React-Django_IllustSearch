import React from 'react';
import { render } from 'react-dom';
import { act, Simulate } from 'react-dom/test-utils';

import * as BaseData from 'Common/BaseData';

import * as LoginData from 'Component/Login/loginData';
import { Login, LoginView } from 'Component/Login/ViewLogin';
import { Setting } from 'settings';
import { Message } from 'message.properties';

import { domTest, asyncDomTest, apiTest } from '../testUtils/testDecorators';
import { getAPIInfo, getSimpleOkResponse } from '../testUtils/testAPIUtils';
import * as TestData from './testData';

// useHistoryのMock化
const historyMock = jest.fn();
jest.mock('react-router-dom', () => ({
    useHistory: () => ({
        push: historyMock
    })
}));

describe('ログインカスタムフックのテスト', () => {

    describe('ユーザ名変更イベント', () => {

        domTest('ユーザ名を変更すると、入力値がstateのユーザ名へ反映されること', (container) => {

            // GIVEN
            const usernameValue = 'a-pompom';

            // Stateが更新されたかどうかはViewだけでは判別できないので、
            // View関数へ渡すフックをテスト用に上書き
            const state = TestData.getInitialState();
            const changeUsername = (event: React.ChangeEvent<HTMLInputElement>) => {
                state.username.value = event.currentTarget.value;
            };
            const hook: LoginData.Hook = {
                state,
                changeUsername,
                changeViewEvent: null,
                loginEvent: null
            };
            const usernameChangeEvent = getUsernameChangeEvnet(container, usernameValue, hook);

            // WHEN
            act(() => {
                usernameChangeEvent();
            });

            // THEN
            expect(state.username.value).toBe(usernameValue);
        });
    });

    describe('ログインイベント', () => {

        asyncDomTest('ログインに成功すると、トップ画面へ遷移すること', async (container) => {

            // GIVEN
            const body: LoginData.PostBody = {username: 'a-pompom'};
            const usersAPIInfo = getUsersAPIInfo();
            const loginAPInfo = getLoginlAPIInfo(
                body
            );
            const usernameChangeEvent = getUsernameChangeEvnet(container, body.username);
            const loginEvent = getLoginEvent(container);

            await apiTest('', async () => {

                // WHEN
                await act( async () => { usernameChangeEvent(); });
                await act( async () => { loginEvent(); });

                // THEN
                expect(historyMock.mock.calls[0][0]).toBe(Setting.VIEW_PATH.TOP);
                historyMock.mockClear();

            }, [usersAPIInfo, loginAPInfo], true);
        }, false);

        asyncDomTest('ログインに失敗すると、一定秒数失敗メッセージが表示されること', async (container) => {

            // GIVEN
            const body: LoginData.PostBody = {username: 'a-pompom'};
            const usersAPIInfo = getUsersAPIInfo();
            const loginAPInfo = getLoginlAPIInfo(
                body,
                {
                    body: {message: Message.Login.Failure, errors: [{fieldName: 'username', message: Message.Login.FailureUsername}] },
                    ok: false,
                    status: 422,
                }
            );
            const usernameChangeEvent = getUsernameChangeEvnet(container, body.username);
            const loginEvent = getLoginEvent(container);

            await apiTest('', async () => {
                // WHEN
                jest.useFakeTimers();
                await act( async () => { usernameChangeEvent(); });
                await act( async () => { loginEvent(); });


                // THEN
                const errorMessageDOM = container.querySelector('.PopupError');
                expect(errorMessageDOM.textContent).toBe(Message.Login.Failure);
                
                // タイマーによる表示なので、一定秒数経過後は、エラーメッセージが非表示となる
                await act (async () => { render(<Login />, container); jest.runAllTimers(); })
                expect(errorMessageDOM).toBeNull;

            }, [usersAPIInfo, loginAPInfo], true);
        }, false);
    });

    describe('画面切替イベント', () => {

        asyncDomTest('画面切替ボタンをクリックすると、ユーザ登録画面へ遷移すること。', async (container) => {

            // GIVEN
            const apiInfo = getUsersAPIInfo();
            const changeViewEvnet = getChangeViewEvent(container);

            await apiTest('', async () => {

                // WHEN
                await act( async () => { changeViewEvnet(); });

                // THEN
                expect(historyMock.mock.calls[0][0]).toBe(Setting.VIEW_PATH.SIGNUP);
                historyMock.mockClear();

            }, [apiInfo], true);
         });
    });
});

// テスト用イベント・モックAPI取得関数
/**
 * ユーザ名変更イベントのレンダリング関数を取得
 * @param container 描画対象DOM要素
 * @param body ユーザ名を格納したPOSTボディ
 */
const getUsernameChangeEvnet = (container: HTMLDivElement, usernameValue: string, hook?: LoginData.Hook) => {
    
    return () => {
        hook ? 
            render(
                <LoginView {...hook} />
                , container
            ) :
            render(
                <Login />
                , container
            );
        const usernameDOM = container.querySelector('#username') as HTMLInputElement;
        usernameDOM.value = usernameValue;

        Simulate.blur(usernameDOM);
    }
};

/**
 * ログインイベントのレンダリング関数を取得
 * 
 * @param container 描画対象DOM要素
 */
const getLoginEvent = (container: HTMLDivElement) => {

    return () => {

        render(
            <Login />
            , container
        );
        // ログイン
        const loginButton = container.querySelector('#loginButton');
        Simulate.click(loginButton);
    };
};

/**
 * 画面切り替えイベントのレンダリング関数を取得
 * 
 * @param container 描画対象DOM要素
 */
const getChangeViewEvent = (container: HTMLDivElement) => {

    return () => {

        render (
            <Login />
            , container
        );
        const changeViewButton = container.querySelector('#changeViewButton');

        Simulate.click(changeViewButton);
    };
};

/**
 * ユーザ一覧API情報を取得
 * API自体は他でテスト済みで、hookのテストには関わらないので、中身は決め打ち
 */
const getUsersAPIInfo = () => {

    return getAPIInfo<null, LoginData.GetResponse>(
        `${Setting.API_ENDPOINT}${Setting.API_PATH.AUTH.LOGIN}`,
        'get',
        {
            ...getSimpleOkResponse(),
            body: {
                message: 'OK',
                users: [
                    {username: 'a-pompom', iconPath: ''}
                ]
            }
        },
        null
    );
};

/**
 * ログインAPIモック情報を取得
 * @param body POSTボディ
 * @param response 期待されるレスポンス
 */
const getLoginlAPIInfo = (body: LoginData.PostBody, response: BaseData.BaseAPIResponse=getSimpleOkResponse()) => {

    return getAPIInfo<LoginData.PostBody, BaseData.BaseAPIResponse>(
        `${Setting.API_ENDPOINT}${Setting.API_PATH.AUTH.LOGIN}`,
        'post',
        response,
        body
    );
};