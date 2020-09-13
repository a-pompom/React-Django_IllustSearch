import React, { useReducer, useEffect } from 'react'

import { useGetAPI, useBaseReducer } from 'Common/useBase';
import * as BaseData from 'Common/BaseData';

import * as TestData from '../TestData';

/**
 * テスト用reducer アクションの発行履歴と、レスポンスの格納を実行
 * 
 * @param state 更新対象の状態
 * @param action 発行されたアクション
 */
const reducer = (state: TestData.GetState, action: TestData.IAction): TestData.GetState => {

    state.actionHisotryList.push(action.type);

    if (action.type === 'GET_SUCCESS_HANDLER' || action.type === 'GET_FAILURE_HANDLER') {
        state.response = action.payload.response;
    }

    return state;
}

/**
 * GET API検証用フック
 * テスト用のAPIを発行
 * 
 * @param argState 更新対象のState
 * @param getParam GET APIへのパラメータ
 */
const useTestForGetAPI = (
    argState: TestData.GetState,
    getPath: string,
    getParam: TestData.GetAPIParam,
    getAPI?: BaseData.GetAPI<TestData.GetAPIParam, TestData.GetResponse>
) => {

    // GET APIの前後処理で利用するreducer
    const reducerWrapper = useBaseReducer<TestData.GetState, TestData.IAction>(reducer);
    const [state, dispatch] = useReducer(reducerWrapper, argState);

    // GET API用フック
    const emitGet = useGetAPI<TestData.GetAPIParam, TestData.GetResponse>(dispatch, getAPI);

    // 初期表示でGET　APIを発行
    useEffect(() => {
        emitGet(
            getPath,
            getParam, 
            {
                handler: ((response, dispatch) => { dispatch( {type: 'GET_SUCCESS_HANDLER', payload: {response} }) }),
                args: [dispatch]
            },
            {
                handler: ((response, dispatch) => { dispatch( {type: 'GET_FAILURE_HANDLER', payload: {response} }) }),
                args: [dispatch]
            }
        );
    }, []);


    return {
        state
    }
}

// GET APIを検証するためのテストコンポーネント
export const ViewTestForGetAPI: React.FC<TestData.ViewTestForGetAPIProps> = ({
    argState,
    getPath,
    getParam,
    getAPI
}) => {

    const {state} = useTestForGetAPI(argState, getPath, getParam, getAPI);

    return (
        <React.Fragment>
            {/* Actionの履歴 */}
            <ul id="ActionHistory">
                {state.actionHisotryList.map(action => {

                    return (
                        <li key={action}>
                            {action}
                        </li>
                    )
                })}
            </ul>

            {/* レスポンス */}
            <p id="ResponseName">
                {state.response ? state.response.body.name : null}
            </p>
            <p id="ResponseAge">
                {state.response ? state.response.body.age : null}
            </p>

        </React.Fragment>
    )
}