import * as BaseData from './BaseData';
import { Field } from './Field';
import { getPropertyByKeyString } from './Logic/objectHandler';

/**
 * ベースとなるreducer 共通処理を事前に実行 主に処理状況を管理するために利用
 * 
 * @param state 更新対象の状態
 * @param action アクション
 */
export const reducer = <State extends BaseData.BaseState>(state: State, action: BaseData.IBaseAction): State => {

    switch(action.type) {
        // Phase
        case 'IDLE':
            state.phase.currentPhase = 'IDLE';
            return state;
        case 'BEFORE_GET':
            state.phase.initialize();
            state.phase.currentPhase = 'LOADING';
            return state;

        case 'BEFORE_POST':
            state.phase.initialize();
            state.phase.currentPhase = 'LOADING';
            return state;
        
        case 'SUCCESS_GET': case 'FAILURE_GET': case 'SUCCESS_POST':
            state.phase.currentPhase = 'IDLE';
            return state;

        case 'FAILURE_POST':
            state.phase.currentPhase = 'FAILURE'
            return state;

        // バリデーション結果反映
        case 'AFTER_VALIDATION':
            action.payload.results.forEach((result) => {

                const oldField = getPropertyByKeyString<State>(state, result.fieldName) as Field<string, unknown>;

                // APIによる検証の場合は、もとの値を保持しないので、更新すると空になる よって、更新値が存在する場合のみ更新
                if (result.fieldValue) {
                    oldField.value = result.fieldValue;
                }
                oldField.errors = result.errors;
            });
            return state;
        
        // ディレイ表示追加
        case 'ADD_TIMER':
            state.phase.addActiveTimer(action.payload.timer);
            return state;

        default:
            return state;
    }
}