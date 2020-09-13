import React, { useReducer, useEffect } from 'react'

import * as BaseData from 'Common/BaseData';
import { Field } from 'Common/Field';
import { Error } from 'Common/Views/ViewError';
import { useValidation, useBaseReducer } from 'Common/useBase';

import * as TestData from '../TestData';

// テスト用reducer Stateを更新するために利用
const reducer = (state: TestData.ValidatorState, action: TestData.IAction): TestData.ValidatorState => {

    return state;
}

/**
 * バリデーション処理本体 テスト用に仮の処理を実行
 * 
 * @param state 相関チェックが必要な場合に用いるState
 * @param field バリデーション処理によって更新されるフィールド
 * @param value バリデーション対象値
 */
const executeValidate = (
    state: TestData.ValidatorState,
    field: Field<TestData.FieldName, TestData.Value>,
    value: TestData.Value,
): BaseData.ValidationResult<TestData.FieldName, TestData.Value>[] => {

    const results = [];

    // 名前
    if (field.name === 'name' && value) {
        field.value = value;
        field.errors = [];

        results.push(field.getValidationResult());
    }
    // 年齢
    if (field.name === 'age' && value) {
        field.value = value;
        field.errors = ['年齢は数値で入力してください。', '年齢は0以上の整数のみ指定できます。']

        // 相関チェック用
        if(state.name.value) {
            state.name.value = '相関チェック値'
            state.name.errors.push('相関チェックエラー');
            results.push(state.name.getValidationResult());
        }

        results.push(field.getValidationResult());
    }

    return results;
};

/**
 * バリデーション処理を実行するためのカスタムフック
 * 
 * @param argState 更新対象State
 * @param fieldNames 更新対象フィールド名を格納したリスト
 * @param fieldValues 更新対象値を格納したリスト
 */
const useTestForValidator = (
    argState: TestData.ValidatorState,
    fieldNames: TestData.FieldName[],
    fieldValues: TestData.Value[]
) => {

    const reducerWrapper = useBaseReducer<TestData.ValidatorState, TestData.IAction>(reducer);
    const [state, dispatch] = useReducer(reducerWrapper, argState);
    // バリデーションフックを用いてバリデーション処理を取得
    const {validate, isValid} = useValidation(executeValidate, ['name', 'age'], dispatch);

    // 個別フィールドバリデーション
    useEffect(() => {

        for (let i=0; i<fieldNames.length; i++) {
            validate(state, fieldNames[i], fieldValues[i]);
        }
    }, []);
    // 全体バリデーション 個別フィールドを検証後に実行
    useEffect(() => {
        state.isValid = isValid(state);

    }, [state.age.value, state.name.value]);

    // コンポーネントで処理結果を表示するためにStateを返却
    return {
        state
    }
}

// バリデーション処理を検証するためのテストコンポーネント
export const ViewTestForValidator: React.FC<TestData.ViewTestForValidatorProps> = ({
    argState,
    fieldNames,
    fieldValues
}) => {

    const {state} = useTestForValidator(argState, fieldNames, fieldValues);

    return (
        <React.Fragment>
            <p id="NameValue">
                {state.name.value}
            </p>
            <p id="NameErrors">
                <Error errors={state.name.errors} />
            </p>
            <p id="AgeValue">
                {state.age.value}
            </p>
            <p id="AgeErrors">
                <Error errors={state.age.errors} />
            </p>

            <p id="IsValid">{String(state.isValid)}</p>
        </React.Fragment>
    )
}