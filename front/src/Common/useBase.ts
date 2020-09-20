import React from 'react';
import { cloneDeep, clone } from 'lodash';

import * as BaseData from './BaseData';
import * as APIHandler from './Logic/apiHandler';
import { Field } from './Field';
import { getPropertyByKeyString } from './Logic/objectHandler';
import { reducer as baseReducer } from './reducer';

/**
 * GetAPIリクエストを発行するためのフック
 * 
 * @param dispatch reducerを呼び出すためのdispatch処理
 * @param getAPI APIリクエストを発行する処理
 * 
 * @return GET APIリクエストを発火させるためのトリガー
 */
export const useGetAPI = <GetAPIArg = {}, GetResponse extends BaseData.BaseAPIResponse=BaseData.BaseAPIResponse>(
    dispatch: React.Dispatch<BaseData.IBaseAction>, 
    getAPI?: BaseData.GetAPI<GetAPIArg, GetResponse>,
) => {

    /**
     * GET APIリクエストを発行
     * 
     * @param getAPIArg GET APIへ渡す引数オブジェクト
     * 
     * @return GET レスポンス
     */
    const executeGet = async (path: string, getAPIArg?: GetAPIArg) => {

        // 指定されたパスへ、クエリ文字列つきのGETリクエストを送信するAPI or ユーザ定義のGET API
        const api = getAPI ? getAPI : APIHandler.get;
        const response = await api(path, getAPIArg);

        // GETリクエストの後処理
        const action: BaseData.AfterGetAction = {
            type: response.ok ? 'SUCCESS_GET' : 'FAILURE_GET',
            payload: {
                response: response
            }
        };
        dispatch(action);

        return response;
    }

    /**
     * GET APIリクエストを呼び元で発火
     * 
     * @param path GET APIリクエスト送信先パス
     * @param getAPIArg GET APIリクエストへ渡す引数オブジェクト
     * @param successHandler リクエスト成功時実行処理
     * @param failureHandler リクエスト失敗時実行処理
     */
    const emitGet = <SuccessHandlerArgs extends any[], FailureHandlerArgs extends any[]>(
        path: string,
        getAPIArg?: GetAPIArg,
        successHandler?: BaseData.GetCallbackHandler<GetResponse, SuccessHandlerArgs>,
        failureHandler?: BaseData.GetCallbackHandler<GetResponse, FailureHandlerArgs>
    ) => {
        
        // 前処理
        const action: BaseData.BeforeGetAction = {
            type: 'BEFORE_GET'
        };
        dispatch(action);

        // GETリクエスト発行後のコールバック処理
        const callbackGet = async () => {

            const response: GetResponse = await executeGet(path, getAPIArg);

            // 成功
            if (response.ok && successHandler) {
                successHandler.handler(response, ...successHandler.args);
                return;
            }
            // 失敗
            if (! response.ok && failureHandler) {
                failureHandler.handler(response, ...failureHandler.args);
                return;
            }
        }

        callbackGet();
    }
    return emitGet;
}

/**
 * 
 * @param dispatch reducerを呼び出すためのdispatch処理
 * @param postAPI APIリクエストを発行する処理
 * 
 * @return
 *     emitPost: POSTリクエストのトリガー フックはTOPレベルでのみ利用できるので、イベントでPOST処理を実行できるようトリガーを返却
 */
export const usePostAPI = <Body, PostResponse extends BaseData.BaseAPIResponse=BaseData.BaseAPIResponse>(
    dispatch: React.Dispatch<BaseData.IBaseAction>, 
    postAPI?: BaseData.PostAPI<Body, PostResponse>
) => {

    /**
     * POSTリクエストを実際に発行
     * 
     * @param body POSTリクエストボディ
     */
    const executePost = async (path: string, body: Body): Promise<PostResponse> => {

        // 指定されたパスへ、ボディつきのリクエストを送信するPOST API or ユーザ定義のPOST API
        const api = postAPI ? postAPI : APIHandler.post;
        const response = await api(path, body);

        // 処理結果をActionを介してStateへ反映
        const action: BaseData.AfterPostAction = {
            type: response.ok ? 'SUCCESS_POST' : 'FAILURE_POST',
            payload: {
                response: response
            }
        };
        dispatch(action);

        return response;
    }

    /**
     * 呼び出し元からPOST処理を発火
     * @param body POSTリクエストボディ
     * @param path POST APIエンドポイント
     * @param successHandler POST成功処理
     * @param failureHandler POST失敗処理
     */
    const emitPost = <SuccessHandlerArgs extends any[], FailureHandlerArgs extends any[]>(
        path: string,
        body: Body,
        successHandler?: BaseData.PostCallbackHandler<SuccessHandlerArgs>,
        failureHandler?: BaseData.PostCallbackHandler<FailureHandlerArgs>
    ) => {

        // POST前処理
        const action: BaseData.BeforePostAction = {
            type: 'BEFORE_POST'
        };
        dispatch(action);

        /**
         * POST処理後に実行 成否に応じてハンドラを実行
         */
        const callbackPost = async () => {

            const response = await executePost(path, body);

            // 成功
            if (response.ok && successHandler) {
                successHandler.handler(response, ...successHandler.args);
                return;
            }
            // 失敗
            if (! response.ok && failureHandler) {
                failureHandler.handler(response, ...failureHandler.args);
                return;
            }
        }
        callbackPost();
    }
    return emitPost;
};

/**
 * バリデーションフックの返却値
 * @param validate バリデーション処理
 * @param isValid 全体をバリデーションし、リクエストを発行しても良い状態か評価する処理
 */
type ValidationHook<State, FieldNames, Values> = {
    validate: {(state: State, fieldname: FieldNames, fieldValue: Values): boolean},
    isValid: {(state: State): boolean}
};

/**
 * 固有のバリデーション処理をもとに、イベントハンドラから呼び出す汎用バリデーション処理を生成
 * 
 * @param executeValidate 個別バリデーション処理 Stateは相関チェック用にディープコピーしたもの
 * @param validationRequiredfields バリデーションが必要なフィールド名文字列 isValid処理の検証対象となる
 * @param dispatch reducerを呼び出すためのdispatch関数
 * @return ValidationHook
 */
export const useValidation = <State, FieldNames extends string, Values >(
    executeValidate: {(state: State, field: Field<FieldNames, Values>, value: Values): BaseData.ValidationResult<FieldNames, Values>[]},
    validationRequiredfields: FieldNames[],
    dispatch: React.Dispatch<BaseData.IBaseAction>
): ValidationHook<State, FieldNames, Values> => {
    /**
     * バリデーション処理
     * 固有のバリデーション処理を汎用的に呼び出せるよう前処理として型を整形
     * 
     * @param state 相関チェック用のState 更新自体はreducerが担う
     * @param fieldName バリデーション対象の種類
     * @param fieldValue バリデーション対象値
     * 
     * @returns エラーあり-> false, エラーなし-> true
     */
    const validate = (state: State, fieldName: FieldNames, fieldValue: Values): boolean => {

        // エラーを詰め込み、State内のフィールド値を更新するためのField要素をname属性をもとに取得
        // また、Stateはreducerでのみ更新されるべきなので、バリデーション用にディープコピーしたものを利用
        const validationState = cloneDeep(state);
        const field = getPropertyByKeyString<State>(validationState, fieldName) as Field<FieldNames, Values>;

        const results = executeValidate(validationState, field, fieldValue);
        const action: BaseData.AfterValidationAction<FieldNames, Values> = {
            type: 'AFTER_VALIDATION',
            payload: {
                results: results
            }
        }
        dispatch(action);

        const isValid = results.filter((result) => ! result.isValid).length === 0;
        return isValid;
    }

    /**
     * APIへリクエストを発行する際、パラメータが有効なものかState全体をバリデーション
     * 
     * @param state 検証対象となる値を格納したState
     */
    const isValid = (state: State): boolean => {

        const validationState = cloneDeep(state);
        let isValid = true;
        const validationResults = [];

        // 検証が必要なフィールド名をもとにvalidate処理と同様の処理を実行
        validationRequiredfields.forEach((fieldName) => {

            const field = cloneDeep(getPropertyByKeyString<State>(validationState, fieldName) as Field<FieldNames, Values>);

            // 既にエラーがある場合は妥当となることはないので、検証不要
            if (field.errors.length !== 0) {
                isValid = false;
                return;
            }

            const results = executeValidate(validationState, field, field.value);
            const hasError = results.filter(result => ! result.isValid).length !== 0;

            // 検証対象に一つでもエラーがあれば妥当ではない
            if (hasError) {
                isValid = false;
            }
            validationResults.concat(results);
        });

        if (isValid) {
            return isValid;
        }

        // isValid処理はPOST直前に呼ばれることを想定しているので、値の更新は必要ない エラーメッセージを追加する場合のみdispatch
        const action: BaseData.AfterValidationAction<FieldNames, Values> = {
            type: 'AFTER_VALIDATION',
            payload: {
                results: validationResults
            }
        }
        dispatch(action);

        return isValid;
    };

    return {
        validate,
        isValid
    }
};;

/**
 * 各reducerを汎用reducerでデコレート
 * 
 * @param childRecuer 個別のreducer
 */
export const useBaseReducer = <State extends BaseData.BaseState, Action extends BaseData.BaseAction<string>>
    (childRecuer?: {(state: State, action: Action): State}
): {(state: State, action: Action): State} => {

    /**
     * useReducerフックのdispatchで実際に呼ばれる処理
     * 
     * @param state 更新対象の状態
     * @param action 更新アクション
     */
    const reducerWrapper = (state: State, action: Action) => {

        /**
         * アクションがベース処理のものか判定
         * 
         * @param action 基底アクション/子要素アクション
         * @return true-> ベースreducerの対象 false-> 対象外
         */
        const isIBaseAction = (action: BaseData.BaseAction<string>): action is BaseData.IBaseAction => {
            return BaseData.I_BASE_ACTIONS.includes(action.type);
        }

        // ReactはStateが同一のオブジェクトだった場合、再描画しないので、再描画されるようディープコピー
        let modState = cloneDeep(state);

        // ベース部分のreducer
        if (isIBaseAction(action)) {
            modState = baseReducer<State>(modState, action);
        }

        // 個別のreducerでStateを更新 ベース部分の更新も上書き可能
        if (childRecuer) {
            modState = childRecuer(modState, action);
        }

        return modState;
    };
    return reducerWrapper;
};