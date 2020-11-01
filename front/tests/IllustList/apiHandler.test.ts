import { handleIllustListGetSuccess } from 'Component/IllustList/apiHandler';

import { getInitAPIData } from './apiHandler.data';

describe('イラスト一覧APIハンドラ', () => {

    describe('初期描画', () => {

        test('イラスト一覧取得APIハンドラで、dispatch関数が初期描画Actionを引数に呼ばれること', () => {

            // GIVEN
            const dispatchMock = jest.fn();
            const { response, expected } = getInitAPIData();

            // WHEN
            handleIllustListGetSuccess(response, dispatchMock);

            // THEN
            expect(dispatchMock.mock.calls[0][0]).toMatchObject(expected);
        });

    });
});