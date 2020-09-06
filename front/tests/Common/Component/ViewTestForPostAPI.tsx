import React, { useReducer, useEffect } from 'react'

import { usePostAPI, useBaseReducer } from 'Common/useBase';
import * as BaseData from 'Common/BaseData';

import * as TestData from '../TestData';

/**
 * テスト用reducer アクションの発行履歴と、レスポンスの格納を実行
 * 
 * @param state 更新対象の状態
 * @param action 発行されたアクション
 */
const reducer = (state: TestData.PostState, action: TestData.IAction): TestData.PostState => {

    state.actionHisotryList.push(action.type);

    if (action.type === 'POST_SUCCESS_HANDLER' || action.type === 'POST_FAILURE_HANDLER') {
        state.response = action.payload.response;
    }

    return state;
}

/**
 * POST API検証用フック
 * テスト用のAPIを発行
 * 
 * @param argState 更新対象のState
 * @param
 */
const useTestForPostAPI = (
    argState: TestData.PostState,
    postPath: string,
    postBody: TestData.PostAPIBody,
    postAPI?: BaseData.PostAPI<TestData.PostAPIBody, BaseData.BaseAPIResponse>
) => {

    // POST APIの前後処理で利用するreducer
    const reducerWrapper = useBaseReducer<TestData.PostState, TestData.IAction>(reducer);
    const [state, dispatch] = useReducer(reducerWrapper, argState);

    // POST API用フック
    const emitPost = usePostAPI<TestData.PostAPIBody>(dispatch, postAPI);

    // 初期表示でPOST APIを発行
    useEffect(() => {
        emitPost(
            postPath,
            postBody, 
            {
                handler: ((response, dispatch) => { dispatch( {type: 'POST_SUCCESS_HANDLER', payload: {response} }) }),
                args: [dispatch]
            },
            {
                handler: ((response, dispatch) => { dispatch( {type: 'POST_FAILURE_HANDLER', payload: {response} }) }),
                args: [dispatch]
            }
        );
    }, []);

    return {
        state
    }
}

// POST APIを検証するためのテストコンポーネント
export const ViewTestForPostAPI: React.FC<TestData.ViewTestForPostAPIProps> = ({
    argState,
    postPath,
    postBody,
    postAPI
}) => {

    const {state} = useTestForPostAPI(argState, postPath, postBody, postAPI);

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
            <p id="ResponseMessage">
                {state.response ? state.response.message : null}
            </p>

        </React.Fragment>
    )
}