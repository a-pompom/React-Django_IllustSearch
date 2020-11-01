import * as IllustData from 'Component/IllustList/illustListData';
import { Phase } from 'Common/Phase';

import * as TestData from './data';
import * as TestUtils from '../testUtils/testAPIUtils';

/**
 * 初期表示用
 * 初期State, Action, 期待結果を返却
 */
export const getInitReducerData = () => {

    const initialState: IllustData.State = {
        illust_list: [],
        phase: new Phase('INIT'),
    };
    const response: IllustData.GetResponse = {
        ...TestUtils.getSimpleOkResponse(),
        body: {
            illust_list: TestData.simpleImageList
        }
    };
    const action = IllustData.illustListGet(response);

    const expected = TestData.simpleImageList;

    return {
        initialState,
        action,
        expected,
    };
};