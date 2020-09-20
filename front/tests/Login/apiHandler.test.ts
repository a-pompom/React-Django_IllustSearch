
import * as H from 'history';
import * as TestUtils from '../testUtils/testAPIUtils';
import * as TestData from './testData';

import { handleUserGetSuccess, handlePostSuccess, handlePostFailure } from 'Component/Login/apiHandler';
import * as LoginData from 'Component/Login/loginData';
import { Setting } from 'settings';


// historyAPIのMock化
const historyMock = jest.fn();
jest.mock('history', () => ({
    createBrowserHistory: () => ({
        push: historyMock
    })
}));

describe('ログイン処理APIハンドラ', () => {

    test('ユーザ取得APIハンドラでレスポンスを格納したActionがDispatchされること', () => {

        // GIVEN
        const dispatchMock = jest.fn();
        const expectedUsers = TestData.users;
        const response: LoginData.GetResponse = {
            ...TestUtils.getSimpleOkResponse(),
            body: {
                message: 'ok',
                users: expectedUsers
            }
        };

        // WHEN
        handleUserGetSuccess(response, dispatchMock);

        // THEN
        expect(dispatchMock.mock.calls[0][0]['type']).toBe('USER_GET');
        expect(dispatchMock.mock.calls[0][0]['payload']['response']['body']['users']).toMatchObject(expectedUsers);
    });

    test('ログイン成功ハンドラでトップ画面へ遷移すること', () => {

        // GIVEN
        const mockHistory = H.createBrowserHistory();

        // WHEN
        handlePostSuccess(null, mockHistory);

        // THEN
        expect(historyMock.mock.calls[0][0]).toBe(Setting.VIEW_PATH.TOP);
    });

    test('ログイン失敗ハンドラでADD_TIMEとIDLEのActionがDispatchされること', () => {

        // GIVEN
        const dispatchMock = jest.fn();
        jest.useFakeTimers();

        // WHEN
        handlePostFailure(null, dispatchMock);
        jest.runAllTimers();

        // THEN
        expect(dispatchMock.mock.calls[0][0]['type']).toBe('ADD_TIMER');
        expect(dispatchMock.mock.calls[1][0]['type']).toBe('IDLE');
    });
});