import React, { useReducer } from 'react';
import { useHistory } from 'react-router-dom';

import * as BaseData from 'Common/BaseData';
import { Field } from 'Common/Field';
import { Phase } from 'Common/Phase';
import * as BaseHook from 'Common/useBase';
import { Setting } from 'settings';

import { getUserList, postLogin, handlePostSuccess, handlePostFailure } from './apiHandler';
import * as LoginData from './loginData';
import { reducer, UsernameChangeAction, IAction } from './reducer';

/**
 * ログイン処理用フック
 * 
 * @remarks ログイン処理に必要なユーザ情報・API呼び出しを管理
 *     更に、今回のアプリは一人でユーザ全体を扱うので、ログインユーザを一覧から選択して
 * ログインするための機能も作成
 * 
 * @returns 状態とイベントハンドラを格納したフック
 */
export const useLogin = (): LoginData.Hook => {

    // 画面表示時の初期状態
    const initialState: LoginData.State = {
        users: [],
        loginUsername: new Field('loginUsername', '', 'ユーザ名'),
        phase: new Phase('INIT')
    };

    const reducerWrapper = BaseHook.useBaseReducer<LoginData.State, IAction>(reducer);
    const [state, dispatch] = useReducer(reducerWrapper, initialState);

    // 画面表示 ログインユーザ一覧を取得
    BaseHook.useGetAPI<LoginData.User[]>(dispatch, getUserList);
    // POST処理
    const emitPost = BaseHook.usePostAPI<LoginData.PostBody>(dispatch, postLogin);

    const history = useHistory();

    // イベントハンドラ

    /**
     * ユーザ名変更イベント ログインユーザ情報を状態として保持
     * @param event 入力内容を格納したイベントオブジェクト
     */
    const changeUsername = (event: React.ChangeEvent<HTMLInputElement>) => {

        const action: UsernameChangeAction = {
            type: 'CHANGE_USER',
            paylodad: {
                username: event.target.value
            }
        };
        dispatch(action);
    };

    /**
     * 画面表示切り替えイベント ユーザ登録画面へ切り替え
     * 
     * @param event イベントオブジェクト
     */
    const changeViewEvent = (event: React.MouseEvent<HTMLElement>) => {

        history.push(Setting.VIEW_PATH.SIGNUP);
    }

    /**
     * ログインイベント APIリクエストで認証に成功したらトップ画面へ遷移
     * 
     * @param event イベントオブジェクト
     */
    const loginEvent: LoginData.LoginEvent = (event) => {

        event.preventDefault();

        const action: BaseData.BeforePostAction = {
            type: 'BEFORE_POST'
        };
        dispatch(action);

        /**
         * POST処理後に実行 ログイン成功の場合はTOP画面へ遷移し、失敗した場合はエラーメッセージを表示
         */
        const callbackPost = async () => {

            const response = await emitPost({username: state.loginUsername.value});

            if (response.ok) {
                handlePostSuccess(history);
                return;
            }
            handlePostFailure(dispatch);
        }

        callbackPost();
    };

    return {
        state,

        changeUsername,
        changeViewEvent,
        loginEvent,
    };
};