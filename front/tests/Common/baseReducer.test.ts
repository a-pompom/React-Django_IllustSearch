import * as BaseData from 'Common/BaseData';
import { Field } from 'Common/Field';
import { reducer } from 'Common/reducer';
import { Phase } from 'Common/Phase';

describe('baseReducer 各アクションのState更新を検証', () => {

    describe('単純なphaseの書き換え', () => {

        // テスト名, アクション, 初期State, 期待結果Phase
        // GIVEN
        type Args = [string, BaseData.IBaseAction, BaseData.BaseState, BaseData.Phase]
        test.each<Args>([
            ['IDLEへ更新 Action:IDLE',             {type: 'IDLE'},                                   {phase: new Phase('INIT')}, 'IDLE'],
            ['IDLEへ更新 Action:SUCCESS_POST',     {type: 'SUCCESS_POST', payload:{response: null}}, {phase: new Phase('INIT')}, 'IDLE'],
            ['IDLEへ更新 Action: SUCCESS_GET',     {type: 'SUCCESS_GET',  payload:{response: null}}, {phase: new Phase('INIT')}, 'IDLE'],
            ['IDLEへ更新 Action: FAILURE_GET',     {type: 'FAILURE_GET',  payload:{response: null}}, {phase: new Phase('INIT')}, 'IDLE'],
            ['FAILUREへ更新 Action: FAILURE_POST', {type: 'FAILURE_POST', payload:{response: null}}, {phase: new Phase('IDLE')}, 'FAILURE'],

        ])('StateのPhaseがアクションと対応したものとなること_%s', (_, action, state, expectedPhase) => {

            // WHEN
            reducer(state, action);

            // THEN
            expect(state.phase.currentPhase).toBe(expectedPhase);
        })
    });

    describe('タイマーの追加', () => {

        test('actionでPhaseのアクティブなタイマーを追加できること', () => {

            // GIVEN
            const action: BaseData.AddTimerAction = {
                type: 'ADD_TIMER',
                payload: {
                    timer: global.setTimeout(() => {}, 0)
                }
            };

            const state: BaseData.BaseState = {
                phase: new Phase('IDLE')
            }

            // WHEN
            reducer(state, action);

            // THEN
            expect(state.phase['_activeTimers'].length).not.toBe(0);
        });

    });

    describe('initializeによるPhaseの初期化', () => {

        // テスト名, アクション, 初期State, 期待結果Phase
        // GIVEN
        type Args = [string, BaseData.BeforeGetAction | BaseData.BeforePostAction, BaseData.BaseState, BaseData.Phase]
        test.each<Args>([
            ['BEFORE_GET',  {type: 'BEFORE_GET'},  {phase: new Phase('IDLE')}, 'LOADING'],
            ['BEFORE_POST', {type: 'BEFORE_POST'}, {phase: new Phase('IDLE')}, 'LOADING'],
        ])('API呼び出しの前処理でPhaseのメッセージとタイマーが初期化されること_%s', (_, action, state, expectedPhase) => {

            state.phase.message= 'Some message';
            state.phase.addActiveTimer(global.setTimeout(() => {}, 0));

            // WHEN
            reducer(state, action);

            // THEN
            expect(state.phase.currentPhase).toBe(expectedPhase);
            expect(state.phase.message).toBe('');
            expect(state.phase['_activeTimers'].length).toBe(0);
        });

    });

    describe('バリデーション結果の反映', () => {

        // GIVEN

        // Stateの形式
        type State = BaseData.BaseState & {

            value?: Field<string, any>,
            nestedValue?: {
                value: Field<string, any>
            }
            nestedAndArrayValue?: {
                nested: {
                    array: [
                        {value: Field<string, any>},
                        {value: Field<string, any>}
                    ]
                }
            }
        };

        // 反映用バリデーション結果 Stateの各要素ごとに定義
        // 1階層/2階層/3階層+配列の要素を取得できるか検証
        const validationResults: {[key: string]: BaseData.ValidationResult<string, string>} = {
            value:                { isValid: true,  fieldName: 'value',                                     fieldValue: 'value',       errors: []},
            nestedValue:          { isValid: false, fieldName: 'nestedValue.value',                         fieldValue: 'nestedValue', errors:['error!!']},
            nestedAndArrayValue1: { isValid: true,  fieldName: 'nestedAndArrayValue.nested.array[0].value', fieldValue: 'value1',      errors: []},
            nestedAndArrayValue2: { isValid: false, fieldName: 'nestedAndArrayValue.nested.array[1].value', fieldValue: 'value2',      errors: ['error1', 'error2']},
        };


        test('Stateへバリデーション結果が反映され、valueとerrorsが更新されること', () => {

            // バリデーション結果反映用アクション Stateの各要素を更新するためのバリデーション結果を格納
            const action: BaseData.AfterValidationAction<string, string> = {
                type: 'AFTER_VALIDATION',
                payload: {
                    results: [validationResults.value, validationResults.nestedValue, validationResults.nestedAndArrayValue1, validationResults.nestedAndArrayValue2]
                }
            };

            // バリデーション結果反映用State
            const state: State = {
                phase: new Phase('IDLE'),
                value: new Field<string, string>('value', '', ''),
                nestedValue: {
                    value: new Field<string, string>('nestedValue.value', '', '')
                },
                nestedAndArrayValue: {
                    nested: {
                        array: [
                            {value: new Field<string, string>('nestedAndArrayValue.nested.array[0].value', '', '')},
                            {value: new Field<string, string>('nestedAndArrayValue.nested.array[1].value', '', '')}
                        ]
                    }
                }
            };

            // WHEN
            reducer(state, action);

            // THEN
            expect(state.value.value).toBe('value');

            expect(state.nestedValue.value.value).toBe('nestedValue');
            expect(state.nestedValue.value.errors[0]).toBe('error!!')

            expect(state.nestedAndArrayValue.nested.array[0].value.value).toBe('value1');
            expect(state.nestedAndArrayValue.nested.array[1].value.value).toBe('value2');
            expect(state.nestedAndArrayValue.nested.array[1].value.errors.length).toBe(2);
        });

    })
});