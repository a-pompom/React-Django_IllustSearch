import React from 'react';
import { render } from 'react-dom';
import { act, Simulate } from 'react-dom/test-utils';

import * as BaseData from 'Common/BaseData';

import * as SignupData from 'Component/Signup/signupData';
import { Signup } from 'Component/Signup/ViewSignup';
import { Setting } from 'settings';
import { Message } from 'message.properties';

import { domTest, asyncDomTest, apiTest } from '../testUtils/testDecorators';
import { getAPIInfo } from '../testUtils/testAPIUtils';

// Mockはモジュールのトップレベルでのみ記述可能
// useHistoryのMock化
const historyMock = jest.fn();
jest.mock('react-router-dom', () => ({
    useHistory: () => ({
        push: historyMock
    })
}));

describe('ユーザ登録カスタムフックのテスト', () => {

    describe('ユーザ名変更イベント', () => {

        // 正常系
        asyncDomTest('重複しないユーザ名の場合、変更時にエラーメッセージが表示されないこと。', async (container) => {

            // GIVEN
            const body: SignupData.PostBody = { username: 'a-pompom'};
            const apiInfo = getValidateUniqueUserAPIInfo(
                {body: {message: 'OK'}, ok: true, status: 200},
                body
            )
            const usernameChangeEvent = getUsernameChangeEvnet(container, body.username);

            await apiTest('', async () => {

                // WHEN
                await act( async () => usernameChangeEvent());

                // THEN
                expect(document.querySelector('.Error')).toBeNull();
            }, [apiInfo], true);

        }, false);

        domTest('ユーザフィールドにエラーが存在するとき、APIが呼ばれないこと', (container) => {

            // GIVEN
            let longUsername = '';
            for (let i=0; i < 1000; i++ ){
                longUsername+= 'x';
            }
            
            const usernameChangeEvent = getUsernameChangeEvnet(container, longUsername);

            // WHEN
            act(usernameChangeEvent);

            // THEN
            expect(document.querySelector('.Error').textContent).toBe(Message.Signup.MaxLength);
        })

        // 重複あり
        asyncDomTest('重複するユーザ名の場合、重複エラーメッセージが表示されること。', async (container) => {

            // GIVEN
            const body: SignupData.PostBody = { username: 'ユーザ'};
            const apiInfo = getValidateUniqueUserAPIInfo(
                {body: {message: 'error', errors: [{fieldName: 'username', message: Message.Signup.Duplicate}] }, ok: false, status: 422},
                body
            )
            const usernameChangeEvent = getUsernameChangeEvnet(container, body.username);

            await apiTest('', async () => {

                // WHEN
                await act( async () => { usernameChangeEvent(); });

                // THEN
                expect(document.querySelector('.Error').textContent).toBe(Message.Signup.Duplicate);
            }, [apiInfo], true);

        }, false);

    });

    describe('ユーザ登録イベント', () => {

        asyncDomTest('登録可能なユーザ名でユーザ登録イベントを発火させると、登録成功の結果としてログイン画面へ遷移すること', async (container) => {

            // GIVEN
            const body: SignupData.PostBody = { username: 'a-pompom'};
            // ユーザ名重複チェックAPI
            const usernameChangeApiInfo = getValidateUniqueUserAPIInfo(
                {body: {message: 'OK'}, ok: true, status: 200},
                body
            )
            const usernameChangeEvent = getUsernameChangeEvnet(container, body.username);

            // ユーザ登録API
            const signupApiInfo = getSignupAPIInfo(
                {body: {message: 'OK'}, ok: true, status: 200},
                body
            );
            const signupEvent = getSignupEvent(container);


            await apiTest('', async () => {

                // WHEN
                await act( async () => { usernameChangeEvent(); });
                await act( async () => { signupEvent(); });

                // THEN
                expect(historyMock.mock.calls[0][0]).toBe(Setting.VIEW_PATH.LOGIN);
                historyMock.mockClear();
            }, [ usernameChangeApiInfo, signupApiInfo], true);

        }, false);

        asyncDomTest('エラーが存在する状態でユーザ登録イベントを発火させると、エラーがそのまま残り、ログイン画面へ遷移しないこと', async (container) => {

            // GIVEN
            const body: SignupData.PostBody = {username: '写真用'};
            // ユーザ名重複チェックAPI
            const usernameChangeApiInfo = getValidateUniqueUserAPIInfo(
                {body: {message: 'error', errors: [{fieldName: 'username', message: Message.Signup.Duplicate}] }, ok: false, status: 422},
                body
            )
            const usernameChangeEvent = getUsernameChangeEvnet(container, body.username);
            const signupEvent = getSignupEvent(container);

            await apiTest('', async () => {

                // WHEN
                await act( async () => { usernameChangeEvent(); });
                await act( async () => { signupEvent(); });

                // THEN
                expect(historyMock.mock.calls).toBeEmpty;
            }, [ usernameChangeApiInfo ], true);

        }, false);
    });

    describe('画面切替イベント', () => {

        domTest('画面切替ボタンをクリックすると、ログイン画面へ遷移すること。', async (container) => {

            // WHEN
            act(() => {
                render(
                    <Signup />
                    , container
                );
                const changeViewButton = container.querySelector('#changeViewButton');

                Simulate.click(changeViewButton);
            });

            // THEN
            expect(historyMock.mock.calls[0][0]).toBe(Setting.VIEW_PATH.LOGIN);
            historyMock.mockClear();
         });
    });
});

// テスト用イベント・APIモック取得用関数
/**
 * ユーザ重複チェックAPIモック情報を取得
 * @param response モックレスポンス
 * @param body POSTボディ
 */
const getValidateUniqueUserAPIInfo = (response: BaseData.BaseAPIResponse, body: SignupData.PostBody) => {

    return getAPIInfo<SignupData.PostBody, BaseData.BaseAPIResponse>(
        `${Setting.API_ENDPOINT}${Setting.API_PATH.AUTH.VALIDATE_UNIQUE_USER}`,
        'post',
        response,
        body
    );
};

/**
 * ユーザ登録APIモック情報を取得
 * @param response モックレスポンス
 * @param body POSTボディ
 */
const getSignupAPIInfo = (response: BaseData.BaseAPIResponse, body: SignupData.PostBody) => {

    return getAPIInfo<SignupData.PostBody, BaseData.BaseAPIResponse>(
        `${Setting.API_ENDPOINT}${Setting.API_PATH.AUTH.SIGNUP}`,
        'post',
        response,
        body
    );
};

/**
 * ユーザ名変更イベントのレンダリング関数を取得
 * @param container 描画対象DOM要素
 * @param body ユーザ名を格納したPOSTボディ
 */
const getUsernameChangeEvnet = (container: HTMLDivElement, usernameValue: string) => {
    
    return () => {
        render(
            <Signup />
            , container
        );
        const usernameDOM = container.querySelector('#username') as HTMLInputElement;
        usernameDOM.value = usernameValue;

        Simulate.blur(usernameDOM);
    }
};

/**
 * ユーザ登録イベントのレンダリング関数を取得
 * 
 * @param container 描画対象DOM要素
 */
const getSignupEvent = (container: HTMLDivElement) => {

    return () => {

        render(
            <Signup />
            , container
        );
        // ユーザ登録
        const signupButton = container.querySelector('#signupButton');
        Simulate.click(signupButton);
    };
};