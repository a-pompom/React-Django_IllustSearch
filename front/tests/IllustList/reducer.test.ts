import { reducer } from 'Component/IllustList/reducer';

import { getInitReducerData } from './reducer.data';

describe('イラスト一覧reducer', () => {

    test('イラスト取得Actionによって、Stateはイラストリストが格納されること', () => {

        // GIVEN
        const { initialState, action, expected} = getInitReducerData();

        // WHEN
        const actual = reducer(initialState, action);

        // THEN
        expect(actual.illust_list).toEqual(expected);
    });
});