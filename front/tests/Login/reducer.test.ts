import { Field } from 'Common/Field';
import { Phase } from 'Common/Phase';
import { Message } from 'message.properties';

import * as TestUtils from '../testUtils/testAPIUtils';
import * as TestData from './testData';

import { reducer } from 'Component/Login/reducer';
import * as LoginData from 'Component/Login/loginData';

describe('Login画面reducer', () => {

    /**
     * 初期Stateを取得
     * 
     * @return ログインState
     */
    const getInitialState = (): LoginData.State => {

        return {
            phase: new Phase('IDLE'),
            username: new Field('username', '', 'ユーザ名'),
            users: []
        };
    };

    test('ユーザ取得Actionによって、Stateへユーザリストが格納されること。', () => {

        // GIVEN
        const state = getInitialState();
        const expectedUsers = TestData.users;

        const response: LoginData.GetResponse = {
            ...TestUtils.getSimpleOkResponse(),
            body: {
                message: 'ok',
                users: expectedUsers
            }
        };
        const action: LoginData.IAction = {
            type: 'USER_GET',
            payload: {
                response
            }
        };

        // WHEN
        reducer(state, action);

        // THEN
        state.users.forEach( (user, index) => {

            expect(user.username).toBe(expectedUsers[index].username);
            expect(user.iconPath).toBe(expectedUsers[index].iconPath);
        });
    });

    test('ユーザ名変更Actionによって、Stateのユーザ名が更新されること。', () => {

        // GIVEN
        const state = getInitialState();
        const expectedUsername = 'a-pompom';
        const action: LoginData.IAction = {
            type: 'CHANGE_USER',
            paylodad: {
                username: expectedUsername
            }
        };

        // WHEN
        reducer(state, action);

        // THEN
        expect(state.username.value).toBe(expectedUsername);
    });

    test('ログイン失敗Actionによって、StateのPhaseメッセージにログイン失敗文字列が格納されること。', () => {

        // GIVEN
        const state = getInitialState();
        const action: LoginData.IAction = {
            type: 'FAILURE_POST',
            payload: {
                response: null,
            }
        };

        // WHEN
        reducer(state, action);

        // THEN
        expect(state.phase.message).toBe(Message.Login.Failure);
    });
});