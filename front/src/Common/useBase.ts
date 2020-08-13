import React, { useEffect } from 'react';
import { cloneDeep } from 'lodash';

import * as BaseData from './BaseData';
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
export const useGetAPI = <GetResponse extends BaseData.BaseGetResponse, GetAPIArgs extends any[]= []>(
    dispatch: React.Dispatch<BaseData.IBaseAction>, 
    getAPI: BaseData.GetAPI<GetAPIArgs, GetResponse>,
) => {

    /**
     * GET APIリクエストを発行
     * 
     * @param getAPIArgs GET APIへ渡す引数
     * 
     * @return GET レスポンス
     */
    const executeGet = async (getAPIArgs: GetAPIArgs) => {
        const response = await getAPI(...getAPIArgs);

        // 処理結果をActionを介してStateへ反映
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
     * @param getAPIArgs GET APIリクエストへ渡す引数
     * @param successHandler リクエスト成功時実行処理
     * @param failureHandler リクエスト失敗時実行処理
     */
    const emitGet = <SuccessHandlerArgs extends any[], FailureHandlerArgs extends any[]>(
        getAPIArgs?: GetAPIArgs,
        successHandler?: BaseData.GetCallbackHandler<SuccessHandlerArgs>,
        failureHandler?: BaseData.GetCallbackHandler<FailureHandlerArgs>) => {
        
        // 前処理
        const action: BaseData.BeforeGetAction = {
            type: 'BEFORE_GET'
        };
        dispatch(action);

        // GETリクエスト発行後のコールバック処理
        const callbackGet = async () => {

            const response: GetResponse = await executeGet(getAPIArgs);

            // 成功
            if (response.ok && successHandler) {
                successHandler.handler(response, ...successHandler.args);
                return;
            }
            // 失敗
            if (failureHandler) {
                failureHandler.handler(response, ...failureHandler.args);
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
export const usePostAPI = <Body>(
    dispatch: React.Dispatch<BaseData.IBaseAction>, 
    postAPI: BaseData.PostAPI<Body>
) => {

    /**
     * POSTリクエストを実際に発行
     * 
     * @param body POSTリクエストボディ
     */
    const executePost = async (body: Body): Promise<BaseData.PostResponse> => {

        const response = await postAPI(body);

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
    const emitPost = <SuccessHandlerArgs extends any[], FailureHandlerArgs extends any[]>(
        body: Body,
        successHandler?: BaseData.PostCallbackHandler<SuccessHandlerArgs>,
        failureHandler?: BaseData.PostCallbackHandler<FailureHandlerArgs>) => {

        const action: BaseData.BeforePostAction = {
            type: 'BEFORE_POST'
        };
        dispatch(action);

        /**
         * POST処理後に実行 ログイン成功の場合はTOP画面へ遷移し、失敗した場合はエラーメッセージを表示
         */
        const callbackPost = async () => {

            const response = await executePost(body);

            if (response.ok && successHandler) {
                successHandler.handler(...successHandler.args);
                return;
            }
            if (failureHandler) {
                failureHandler.handler(...failureHandler.args);
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
interface ValidationHook<State, FieldName, Value> {
    validate: {(state: State, fieldname: FieldName, fieldValue: Value)},
    isValid: {(state: State): boolean}
}

/**
 * 固有のバリデーション処理をもとに、イベントハンドラから呼び出す汎用バリデーション処理を生成
 * 
 * @param executeValidate 個別バリデーション処理
 * @param validationRequiredfields バリデーションが必要なフィールド名文字列 isValid処理の検証対象となる
 * @return ValidationHook
 */
export const useValidation = <State, FieldName extends string, Value>(
    executeValidate: {(state: State, field: Field<Value, FieldName>, value: Value): void},
    validationRequiredfields: FieldName[]
): ValidationHook<State, FieldName, Value> => {
    /**
     * バリデーション処理
     * 固有のバリデーション処理を汎用的に呼び出せるよう前処理として型を整形
     * 
     * @param state 更新対象の状態
     * @param fieldName バリデーション対象の種類
     * @param fieldValue バリデーション対象値
     */
    const validate = (state: State, fieldName: FieldName, fieldValue: Value): void => {

        // エラーを詰め込み、State内のフィールド値を更新するためのField要素をname属性をもとに取得
        const field = getPropertyByKeyString<State>(state, fieldName) as Field<Value, FieldName>;

        executeValidate(state, field, fieldValue);
    }

    /**
     * APIへリクエストを発行する際、パラメータが有効なものかState全体をバリデーション
     * 
     * @param state 検証対象となる値を格納したState
     */
    const isValid = (state: State): boolean => {

        let isValid = true;

        // 検証が必要なフィールド名をもとにvalidate処理と同様の処理を実行
        validationRequiredfields.forEach((fieldName) => {

            const field = getPropertyByKeyString<State>(state, fieldName) as Field<Value, FieldName>;
            executeValidate(state, field, field.value);

            // 検証対象に一つでもエラーがあれば妥当ではない
            if (field.errors.length !== 0) {
                isValid = false;
            }
        });

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
export const useBaseReducer = <ChildState extends BaseData.BaseState, ChildAction extends BaseData.BaseAction<string>>
    (childRecuer: {(state: ChildState, action: ChildAction): ChildState}
): {(state: ChildState, action: ChildAction): ChildState} => {

    /**
     * useReducerフックのdispatchで実際に呼ばれる処理
     * 
     * @param state 更新対象の状態
     * @param action 更新アクション
     */
    const reducerWrapper = (state: ChildState, action: ChildAction) => {

        /**
         * アクションがベース処理のものか判定
         * 
         * @param action 基底アクション/子要素アクション
         * @return true-> ベースreducerの対象 false-> 対象外
         */
        const isIBaseAction = (action: BaseData.BaseAction<string>): action is BaseData.IBaseAction => {
            if (BaseData.I_BASE_ACTIONS.includes(action.type)) {
                return true;
            }
            return false;
        }

        let modState = cloneDeep(state);

        // ベース部分のreducer
        if (isIBaseAction(action)) {
            modState = baseReducer<ChildState>(modState, action);
        }

        // 個別のreducerでStateを更新 ベース部分の更新も上書き可能
        modState = childRecuer(modState, action);

        return modState;
    };
    return reducerWrapper;
};