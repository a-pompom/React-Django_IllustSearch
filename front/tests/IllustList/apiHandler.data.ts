import * as IllustData from 'Component/IllustList/illustListData';

import * as TestData from './data';
import * as TestUtils from '../testUtils/testAPIUtils';

/**
 * イラスト取得API用
 * APIレスポンス, 期待結果を返却
 */
export const getInitAPIData = () => {

    const response: IllustData.GetResponse = {
        ...TestUtils.getSimpleOkResponse(),
        body: {
            illust_list: TestData.simpleImageList
        }
    };
    const expected = IllustData.illustListGet(response);

    return {
        response,
        expected,
    };
};