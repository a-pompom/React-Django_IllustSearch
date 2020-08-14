import React, { useReducer } from 'react';
import { useHistory } from 'react-router-dom';

import * as BaseAPIHandler from 'Common/Logic/apiHandler';
import { Field } from 'Common/Field';
import { Phase } from 'Common/Phase';
import * as BaseHook from 'Common/useBase';
import { Setting } from 'settings';

import { postUserCreate, handleValidateUniqueUserFailure } from './apiHandler';
import * as SignupData from './signupData';
import { reducer } from './reducer';

/**
 * ユーザ登録処理用フック
 * 
 * @returns 状態とイベントハンドラを格納したフック
 */
export const useSignup = (): SignupData.Hook => {
    
    // 画面表示時の初期状態
    const initialState: SignupData.State = {
        username: new Field('username', '', 'ユーザ名'),
        phase: new Phase('IDLE')
    };

    const reducerWrapper = BaseHook.useBaseReducer<SignupData.State, SignupData.IAction>(reducer);
    const [state, dispatch] = useReducer(reducerWrapper, initialState);

    // POST処理
    const emitPost = BaseHook.usePostAPI<SignupData.PostBody>(dispatch, postUserCreate);
    const emitUserUniquePost = BaseHook.usePostAPI<SignupData.PostBody>(dispatch, BaseAPIHandler.post);

    const history = useHistory();

    /**
     * 画面表示切り替えイベント ログイン画面へ切り替え
     * 
     * @param event イベントオブジェクト
     */
    const changeViewEvent = (event: React.MouseEvent<HTMLElement>) => {

        history.push(Setting.VIEW_PATH.LOGIN);
    }

    /**
     * ユーザ登録イベント 登録後、ユーザをログインユーザ一覧へ追加
     * 
     * @param event イベントオブジェクト
     */
    const createUserEvent: SignupData.CreateUserEvent = (event) => {

        event.preventDefault();
    }

    /**
     * ユーザ名変更イベント 重複チェックを実行
     * 
     * @param event イベントオブジェクト
     */
    const changeUsernameEvent: SignupData.ChangeUsernameEvent = (event) => {

        // 入力値をStateへ反映し、エラーを初期化
        const action: SignupData.UsernameChangeAction = {
            type: 'CHANGE_USER',
            paylodad: {
                username: event.target.value
            }
        }
        dispatch(action);

        // 重複チェック 重複している場合はエラーメッセージを表示
        emitUserUniquePost(
            {username: event.target.value}, 
            Setting.API_PATH.VALIDATE_UNIQUE_USER,
            null,
            {
                handler: handleValidateUniqueUserFailure,
                args: [dispatch]
            });
    }

    return {
        state,

        changeUsernameEvent,
        changeViewEvent,
        createUserEvent
    };
};