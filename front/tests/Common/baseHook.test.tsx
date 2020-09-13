import React from 'react';
import { render } from 'react-dom';
import { act } from 'react-dom/test-utils';

import { domTest, domTestEach, APIMockInfo, apiTest } from '../testUtils/testDecorators';

import * as BaseData from 'Common/BaseData';
import * as FetchUtil from 'Common/FetchUtil';
import { ViewTestForReducer } from './Component/ViewTestForReducer';
import { ViewTestForValidator } from './Component/ViewTestForValidator';
import { ViewTestForGetAPI } from './Component/ViewTestForGetAPI';
import { ViewTestForPostAPI } from './Component/ViewTestForPostAPI';
import * as TestData from './TestData';
import { Phase } from 'Common/Phase';
import { Field } from 'Common/Field';

import { Setting } from 'settings';

describe('カスタムフックの動作検証', () => {

    // ラップしたchildReducerが呼ばれること, baseReducerが呼ばれるかを検証
    describe('reducerをラップしたbaseReducerの検証', () => {

        // ラップされるreducer メッセージを設定することで、実行されたことを保証
        const childReducer = (state: TestData.State, action: TestData.IAction) => {
            
            state.phase.message = `${action.type}_message`

            return state;
        }
        // 上書き用reducer 親reducerよりも後に実行されることを保証するため、Stateを上書き
        const childReducerForOverWrite = (state: TestData.State, action: TestData.IAction) => {
            
            state.phase.message = `${action.type}_message`
            state.phase.currentPhase = 'FATAL';

            return state;
        }


        // テスト用コンポーネントへ描画されたPhase・Messageを取得するためのセレクタ
        const phaseSelector = '#Phase';
        const messageSelector = '#Message';

        // テスト名, state, action, Phase文字列, メッセージ
        type BaseReducerArgs = [string, TestData.State, TestData.IAction, BaseData.Phase, string]

        // BaseReducerを介して、Stateが更新されるか
        // GIVEN
        domTestEach<BaseReducerArgs>([

            ['IDLE', {phase: new Phase('IDLE')}, {type: 'IDLE'}, 'IDLE', 'IDLE_message'],
            ['BEFORE_GET', {phase: new Phase('IDLE')}, {type: 'BEFORE_GET'}, 'LOADING', 'BEFORE_GET_message'],
            ['BEFORE_POST', {phase: new Phase('IDLE')}, {type: 'BEFORE_POST'}, 'LOADING', 'BEFORE_POST_message'],
            ['SUCCESS_GET', {phase: new Phase('LOADING')}, {type: 'SUCCESS_GET', payload: null}, 'IDLE', 'SUCCESS_GET_message'],
            ['FAILURE_GET', {phase: new Phase('LOADING')}, {type: 'FAILURE_GET', payload: null}, 'IDLE', 'FAILURE_GET_message'],
            ['SUCCESS_POST', {phase: new Phase('LOADING')}, {type: 'SUCCESS_POST', payload: null}, 'IDLE', 'SUCCESS_POST_message'],
            ['FAILURE_POST', {phase: new Phase('LOADING')}, {type: 'FAILURE_POST', payload: null}, 'FAILURE', 'FAILURE_POST_message'],
            ['AFTER_VALIDATION', {phase: new Phase('IDLE')}, {type: 'AFTER_VALIDATION', payload: {results: []}}, 'IDLE', 'AFTER_VALIDATION_message'],
            ['ADD_TIMER', {phase: new Phase('IDLE')}, {type: 'ADD_TIMER', payload: {timer: null}}, 'IDLE', 'ADD_TIMER_message'],

        ], 'BaseReducerを介してStateが更新されること_%s', (container, _, state, action, phase, message) => {

            // WHEN
            act(() => {
                render(
                    <ViewTestForReducer
                        argState={state}
                        argAction={action}
                        reducer={childReducer}
                     />
                    , container
                );
            });

            // THEN
            const actual = {
                phase: document.querySelector(phaseSelector), 
                message: document.querySelector(messageSelector)
            };
            expect(actual.phase.textContent).toBe(phase);
            expect(actual.message.textContent).toBe(message);
        });

        domTest('子要素のactionがreducerで実行されること。', (container) => {

            // GIVEN
            const state: TestData.State = {
                phase: new Phase('INIT')
            };
            const action: TestData.IAction = {
                type: 'CHILD_ACTION'
            };

            // WHEN
            act(() => {
                render(
                    <ViewTestForReducer
                        argState={state}
                        argAction={action}
                        reducer={childReducer}
                     />
                    , container
                );
            });

            // THEN
            const actual = {
                phase: document.querySelector(phaseSelector), 
                message: document.querySelector(messageSelector)
            };
            expect(actual.phase.textContent).toBe('INIT');
            expect(actual.message.textContent).toBe('CHILD_ACTION_message');
        });

        domTest('子要素のActionが親要素よりも後に実行されることにより、Phaseを上書きできること。', (container) => {

            // GIVEN
            const state: TestData.State = {
                phase: new Phase('INIT')
            };
            const action: TestData.IAction = {
                type: 'IDLE'
            };

            // WHEN
            act(() => {
                render(
                    <ViewTestForReducer
                        argState={state}
                        argAction={action}
                        reducer={childReducerForOverWrite}
                     />
                    , container
                );
            });

            // THEN
            const actual = {
                phase: document.querySelector(phaseSelector), 
                message: document.querySelector(messageSelector)
            };
            expect(actual.phase.textContent).toBe('FATAL');
            expect(actual.message.textContent).toBe('IDLE_message');
        });
    });


    describe('バリデーション処理を担うValidatorの検証', () => {

        // テストコンポーネントの描画結果を取得するためのセレクタ
        const nameValueSelector = "#NameValue";
        const nameErrorsSelector = "#NameErrors";
        const ageValueSelector = "#AgeValue";
        const ageErrorsSelector = "#AgeErrors";
        const isValidSelector = "#IsValid";

        domTest('name属性のみを検証すると、値が格納され、エラーが存在しないこと。', (container) => {

            // GIVEN
            const state: TestData.ValidatorState = {
                phase: new Phase('IDLE'),
                name: new Field('name', '', ''),
                age: new Field('age', null, ''),
                isValid: null
            };
            const expectedNameValue = 'JohnDoe';

            // WHEN
            act(() => {
                render(
                    <ViewTestForValidator
                        argState={state}
                        fieldNames={['name']}
                        fieldValues={[expectedNameValue]}
                     />
                    , container
                );
            });

            // THEN
            const actual = {
                nameValue: document.querySelector(nameValueSelector),
                nameErrors: document.querySelector(nameErrorsSelector),
                isValid: document.querySelector(isValidSelector)
            };

            expect(actual.nameValue.textContent).toBe(expectedNameValue);
            expect(actual.nameErrors.childNodes.length).toBe(0);
            expect(actual.isValid.textContent).toBe('true');
        });

        domTest('age属性のみを検証すると、エラーが存在すること。', (container) => {

            // GIVEN
            const state: TestData.ValidatorState = {
                phase: new Phase('IDLE'),
                name: new Field('name', '', ''),
                age: new Field('age', null, ''),
                isValid: null
            };
            const expectedAgeValue = 9999;
            const expectedAgeErrors = ['年齢は数値で入力してください。', '年齢は0以上の整数のみ指定できます。'];

            // WHEN
            act(() => {
                render(
                    <ViewTestForValidator
                        argState={state}
                        fieldNames={['age']}
                        fieldValues={[expectedAgeValue]}
                     />
                    , container
                );
            });

            // THEN
            const actual = {
                ageValue: document.querySelector(ageValueSelector),
                ageErrors: document.querySelector(ageErrorsSelector),
                isValid: document.querySelector(isValidSelector)
            };

            expect(actual.ageValue.textContent).toBe(String(expectedAgeValue));
            actual.ageErrors.childNodes.forEach((error, index) => {
                expect(error.textContent).toBe(expectedAgeErrors[index]);

            });
            expect(actual.isValid.textContent).toBe('false');
        });

        domTest('name属性とage属性を同時に検証すると、エラーが存在し、相関チェックが働くこと。', (container) => {

            // GIVEN
            const state: TestData.ValidatorState = {
                phase: new Phase('IDLE'),
                name: new Field('name', '', ''),
                age: new Field('age', null, ''),
                isValid: null
            };
            const expectedAgeValue = 20;
            const expectedNameValue = '相関チェック値';
            const expectedNameErrors = ['相関チェックエラー'];

            // WHEN
            act(() => {
                render(
                    <ViewTestForValidator
                        argState={state}
                        fieldNames={['name', 'age']}
                        fieldValues={[expectedNameValue, expectedAgeValue]}
                     />
                    , container
                );
            });

            // THEN
            const actual = {
                nameValue: document.querySelector(nameValueSelector),
                nameErrors: document.querySelector(nameErrorsSelector),
                ageValue: document.querySelector(ageValueSelector),
                ageErrors: document.querySelector(ageErrorsSelector),

                isValid: document.querySelector(isValidSelector)
            };

            expect(actual.isValid.textContent).toBe('false');

            // 相関チェックが有効か
            expect(actual.nameValue.textContent).toBe(expectedNameValue);
            actual.nameErrors.childNodes.forEach((error, index) => {
                expect(error.textContent).toBe(expectedNameErrors[index]);

            });
        });
    });

    describe('GET APIのハンドラを検証', () => {

        const GET_PATH = 'get/';

        // GIVEN
        const user = {name: 'JohnDoe', age: 20};
        const apiInfo: APIMockInfo<TestData.GetResponse, TestData.GetAPIParam> = {
            PATH: `${Setting.API_ENDPOINT}${GET_PATH}`,
            method: 'get',
            expectedResponse: {body: {name: user.name, age: user.age, message: ''}, ok: true, status: 200},
            body: user
        };

        const state: TestData.GetState = {
            phase: new Phase('IDLE'),
            actionHisotryList: [],
            response: null
        };

        domTest('', (container) => {

            apiTest('GETAPIを発行すると、レスポンスが得られること。', async () => {

                // WHEN
                await act( async() => {
                    render(
                        <ViewTestForGetAPI
                            argState={state}
                            getPath={GET_PATH}
                            getParam={user}
                        />
                        , container
                    );
                });

                // THEN
                expect(container.querySelector('#ResponseName').textContent).toBe(apiInfo.expectedResponse.body.name);
                expect(container.querySelector('#ResponseAge').textContent).toBe(String(apiInfo.expectedResponse.body.age));

            }, [apiInfo]);
        }, true);

        domTest('', container => {

            apiTest('GETAPIを実行すると、送信前・送信後・ハンドラそれぞれでActionが発行されていること。', async () => {

                // WHEN
                await act( async() => {
                    render(
                        <ViewTestForGetAPI
                            argState={state}
                            getPath={GET_PATH}
                            getParam={user}
                        />
                        , container
                    );
                });

                // THEN
                const expectedActionHistoryList = ['BEFORE_GET', 'SUCCESS_GET', 'GET_SUCCESS_HANDLER'];
                container.querySelector('#ActionHistory').childNodes.forEach((action, index) => {

                    expect(action.textContent).toBe(expectedActionHistoryList[index]);
                });

            }, [apiInfo]);
        }, true)

        // デフォルトのGET APIを上書き
        domTest('', container => {

            // GIVEN
            // 上書きのテストケースとして、外部APIを発行する場合を想定
            const externalGet = async<Response extends BaseData.BaseAPIResponse, Param={}>(
                apiPath: string,
            ): Promise<Response> => {

                const response = await FetchUtil.get<Response>(`external/${apiPath}`);
                // response.okはPromiseをrejectしない限りはfalseにならないので、手動で設定
                response.ok=false;
                return response;
            };

            const externalApiInfo: APIMockInfo<TestData.GetResponse, TestData.GetAPIParam> = {
                PATH: `external/api/`,
                method: 'get',
                expectedResponse: {body: {name: user.name, age: user.age, message: ''}, ok: false, status: 401},
            } 

            apiTest('定義したGET APIによって、デフォルトのGET APIを上書きできること。', async () => {

                // WHEN
                await act( async() => {
                    render(
                        <ViewTestForGetAPI
                            argState={state}
                            getPath={'api/'}
                            getParam={user}
                            getAPI={externalGet}
                        />
                        , container
                    );
                });

                // THEN
                expect(container.querySelector('#ResponseName').textContent).toBe(apiInfo.expectedResponse.body.name);
                expect(container.querySelector('#ResponseAge').textContent).toBe(String(apiInfo.expectedResponse.body.age));

                const expectedActionHistoryList = ['BEFORE_GET', 'FAILURE_GET', 'GET_FAILURE_HANDLER'];
                container.querySelector('#ActionHistory').childNodes.forEach((action, index) => {

                    expect(action.textContent).toBe(expectedActionHistoryList[index]);
                });

            }, [externalApiInfo]);
        }, true)
    });

    describe('POST APIのハンドラを検証', () => {
        const POST_PATH = 'post/';
        const responseMessage = 'Post OK';

        // GIVEN
        const body: TestData.PostAPIBody = { productName: 'app001', price: 9999};
        const apiInfo: APIMockInfo<TestData.PostResponse, TestData.PostAPIBody> = {
            PATH: `${Setting.API_ENDPOINT}${POST_PATH}`,
            method: 'post',
            expectedResponse: {body: {message: responseMessage}, ok: true, status: 200},
            body: body
        } 

        const state: TestData.PostState = {
            phase: new Phase('IDLE'),
            actionHisotryList: [],
            response: null
        };

        domTest('', (container) => {

            apiTest('POSTAPIを発行すると、レスポンスが得られること。', async () => {

                // WHEN
                await act( async() => {
                    render(
                        <ViewTestForPostAPI
                            argState={state}
                            postPath={POST_PATH}
                            postBody={body}
                        />
                        , container
                    );
                });

                // THEN
                expect(container.querySelector('#ResponseMessage').textContent).toBe(apiInfo.expectedResponse.body.message);

            }, [apiInfo]);
        }, true);

        domTest('', container => {

            apiTest('POST_APIを実行すると、送信前・送信後・ハンドラそれぞれでActionが発行されていること。', async () => {

                // WHEN
                await act( async() => {
                    render(
                        <ViewTestForPostAPI
                            argState={state}
                            postPath={POST_PATH}
                            postBody={body}
                        />
                        , container
                    );
                });

                // THEN
                const expectedActionHistoryList = ['BEFORE_POST', 'SUCCESS_POST', 'POST_SUCCESS_HANDLER'];
                container.querySelector('#ActionHistory').childNodes.forEach((action, index) => {

                    expect(action.textContent).toBe(expectedActionHistoryList[index]);
                });

            }, [apiInfo]);
        }, true);

        // デフォルトのPOST APIを上書き
        domTest('', container => {

            // GIVEN
            // 上書きのテストケースとして、外部APIを発行する場合を想定
            const externalPost = async<Body, Response extends BaseData.BaseAPIResponse>(
                apiPath: string,
                body: Body
            ): Promise<Response> => {

                const response = await FetchUtil.post<Body, Response>(`external/${apiPath}`, body);
                // response.okはPromiseをrejectしない限りはfalseにならないので、手動で設定
                response.ok=false;
                return response;
            };

            const externalApiInfo: APIMockInfo<TestData.PostResponse, TestData.PostAPIBody> = {
                PATH: `external/api/`,
                method: 'post',
                expectedResponse: {body: {message: responseMessage}, ok: false, status: 401},
            } 

            apiTest('定義したPOST APIによって、デフォルトのPOST APIを上書きできること。', async () => {

                // WHEN
                await act( async() => {
                    render(
                        <ViewTestForPostAPI
                            argState={state}
                            postPath={'api/'}
                            postBody={body}
                            postAPI={externalPost}
                        />
                        , container
                    );
                });

                // THEN
                expect(container.querySelector('#ResponseMessage').textContent).toBe(apiInfo.expectedResponse.body.message);

                const expectedActionHistoryList = ['BEFORE_POST', 'FAILURE_POST', 'POST_FAILURE_HANDLER'];
                container.querySelector('#ActionHistory').childNodes.forEach((action, index) => {

                    expect(action.textContent).toBe(expectedActionHistoryList[index]);
                });

            }, [externalApiInfo]);
        }, true);
    });
});