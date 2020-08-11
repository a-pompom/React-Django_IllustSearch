import * as BaseData from './BaseData';
/**
 * ベースとなるreducer 共通処理を事前に実行 主に処理状況を管理するために利用
 * 
 * @param state 更新対象の状態
 * @param action アクション
 */
export const reducer = <State extends BaseData.BaseState>(state: State, action: BaseData.IBaseAction): State => {

    switch(action.type) {
        case 'IDLE':
            state.phase.currentPhase = 'IDLE';
            return state;

        case 'BEFORE_POST':
            state.phase.initialize();
            state.phase.currentPhase = 'LOADING';
            return state;
        
        case 'FETCH_SUCCESS': case 'SUCCESS_POST':
            state.phase.currentPhase = 'IDLE';
            return state;

        case 'FAILURE_POST':
            state.phase.currentPhase = 'FAILURE'
            return state;

        case 'ADD_TIMER':
            state.phase.addActiveTimer(action.payload.timer);
            return state;
        default:
            return state;
    }
}