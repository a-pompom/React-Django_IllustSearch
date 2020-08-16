import React, { useReducer } from 'react';
import { useHistory } from 'react-router-dom';

import * as BaseAPIHandler from 'Common/Logic/apiHandler';
import { Field } from 'Common/Field';
import { Phase } from 'Common/Phase';
import * as BaseHook from 'Common/useBase';
import { Setting } from 'settings';

import { handleValidateUniqueUserFailure, handleSuccessUserCreate } from './apiHandler';
import * as SignupData from './signupData';
import { reducer } from './reducer';
import { executeValidate } from './validator';

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

    // reducer
    const reducerWrapper = BaseHook.useBaseReducer<SignupData.State, SignupData.IAction>(reducer);
    const [state, dispatch] = useReducer(reducerWrapper, initialState);

    // POST処理
    const emitPost = BaseHook.usePostAPI<SignupData.PostBody>(dispatch, BaseAPIHandler.post);
    const emitUserUniquePost = BaseHook.usePostAPI<SignupData.PostBody>(dispatch, BaseAPIHandler.post);

    // バリデーション
    const {validate, isValid} = BaseHook.useValidation<SignupData.State, SignupData.FieldName, SignupData.Value>(
        executeValidate,
        [state.username.name],
        dispatch
    );

    const history = useHistory();

    // イベントハンドラ
    /**
     * ユーザ名変更イベント 重複チェックを実行
     * 
     * @param event イベントオブジェクト
     */
    const changeUsernameEvent: SignupData.ChangeUsernameEvent = (event) => {

        const fieldName = event.target.name as SignupData.FieldName;

        if (! validate(state, fieldName, event.target.value)) {
            return;
        }

        // 重複チェック 重複している場合はエラーメッセージを表示
        emitUserUniquePost(
            {username: event.target.value}, 
            Setting.API_PATH.VALIDATE_UNIQUE_USER,
            null,
            {
                handler: handleValidateUniqueUserFailure,
                args: [fieldName, dispatch]
            });
    }

    /**
     * ユーザ登録イベント 登録後、ユーザをログインユーザ一覧へ追加
     * 
     * @param event イベントオブジェクト
     */
    const createUserEvent: SignupData.CreateUserEvent = (event) => {

        event.preventDefault();

        if (! isValid(state)) {
            return;
        }

        emitPost(
            {username: state.username.value},
            Setting.API_PATH.SIGNUP,
            {
                handler: handleSuccessUserCreate,
                args: [history]
            }
        );
    }
    
    /**
     * 画面表示切り替えイベント ログイン画面へ切り替え
     * 
     * @param event イベントオブジェクト
     */
    const changeViewEvent = (event: React.MouseEvent<HTMLElement>) => {

        history.push(Setting.VIEW_PATH.LOGIN);
    }


    return {
        state,

        changeUsernameEvent,
        createUserEvent,
        changeViewEvent,
    };
};