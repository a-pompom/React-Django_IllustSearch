import React, { useReducer, useEffect } from 'react'

import { useBaseReducer } from 'Common/useBase';

import * as TestData from '../TestData';

/**
 * ReducerWrapper検証用カスタムフック
 * ReducerWrapperを取得し、引数のActionをそのままdsipatchすることで、
 * Stateを更新
 * 
 * @param argState 更新対象State
 * @param argAction 更新内容を格納したアクション
 * @param reducer 子要素Reducer BaseReducer実行後に処理される
 * 
 * @return State 更新後の状態
 */
const useTestForReducer = (
    argState: TestData.State,
    argAction: TestData.IAction,
    reducer: (state: TestData.State, action: TestData.IAction)=> TestData.State
) => {

    // reducer・Stateを初期化
    const reducerWrapper = useBaseReducer<TestData.State, TestData.IAction>(reducer);
    const [state, dispatch] = useReducer(reducerWrapper, argState);

    // 初回描画の際、引数をもとにStateを更新
    useEffect(() => {

        dispatch(argAction);
    }, []);

    return {
        state
    }
}

// ReducerWrapper検証用のテストコンポーネント
// BaseReducerによってPhase/Messageが想定通りに更新されたか検証するために利用
export const ViewTestForReducer: React.FC<TestData.ViewTestForReducerProps> = ({
    argState,
    argAction,
    reducer
}) => {

    const {state} = useTestForReducer(argState, argAction, reducer);

    return (
        <React.Fragment>
            <p id="Phase">
                {state.phase.currentPhase}
            </p>
            <p id="Message">
                {state.phase.message}
            </p>
        </React.Fragment>
    )
}