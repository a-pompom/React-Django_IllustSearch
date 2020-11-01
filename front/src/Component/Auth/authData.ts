import * as BaseData from 'Common/BaseData';

// 画面で管理する状態
export type State = BaseData.BaseState & {};

// Hook 状態を管理
export type Hook = {
    state: State,
};