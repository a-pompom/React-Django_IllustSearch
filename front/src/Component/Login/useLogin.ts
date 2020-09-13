import React, { useReducer, useEffect } from 'react';
import { useHistory } from 'react-router-dom';

import { Field } from 'Common/Field';
import { Phase } from 'Common/Phase';
import * as BaseHook from 'Common/useBase';
import { Setting } from 'settings';

import { getUserList, postLogin, handleGetSuccess, handlePostSuccess, handlePostFailure } from './apiHandler';
import * as LoginData from './loginData';
import { reducer } from './reducer';

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
        username: new Field('username', '', 'ユーザ名'),
        phase: new Phase('INIT')
    };

    const reducerWrapper = BaseHook.useBaseReducer<LoginData.State, LoginData.IAction>(reducer);
    const [state, dispatch] = useReducer(reducerWrapper, initialState);

    // 画面表示 ログインユーザ一覧を取得
    const emitGet = BaseHook.useGetAPI<LoginData.GetResponse>(dispatch, getUserList);
    // POST処理
    const emitPost = BaseHook.usePostAPI<LoginData.PostBody>(dispatch, postLogin);

    const history = useHistory();

    useEffect(() => {

        emitGet(null, {
                handler: handleGetSuccess,
                args: [dispatch]
            }
        );
    }, []);

    // イベントハンドラ

    /**
     * ユーザ名変更イベント ログインユーザ情報を状態として保持
     * @param event 入力内容を格納したイベントオブジェクト
     */
    const changeUsername = (event: React.ChangeEvent<HTMLInputElement>) => {

        const action: LoginData.UsernameChangeAction = {
            type: 'CHANGE_USER',
            paylodad: {
                username: event.target.value
            }
        };
        dispatch(action);
    };

    /**
     * ログインイベント APIリクエストで認証に成功したらトップ画面へ遷移
     * 
     * @param event イベントオブジェクト
     */
    const loginEvent: LoginData.LoginEvent = (event) => {

        event.preventDefault();

        // POST処理実行
        emitPost(
            {username: state.username.value},
            null,
            {
                handler: handlePostSuccess,
                args: [history]
            },
            {
                handler: handlePostFailure,
                args: [dispatch]
            }
        );
    };
    
    /**
     * 画面表示切り替えイベント ユーザ登録画面へ切り替え
     * 
     * @param event イベントオブジェクト
     */
    const changeViewEvent = (event: React.MouseEvent<HTMLElement>) => {

        history.push(Setting.VIEW_PATH.SIGNUP);
    }


    return {
        state,

        changeUsername,
        changeViewEvent,
        loginEvent,
    };
};