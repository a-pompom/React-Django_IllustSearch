import { act } from 'react-dom/test-utils';
import { asyncDomTest, apiTest } from '../testUtils/testDecorators';
import { hookTest } from '../testUtils/testForCommon';

import { Setting } from 'settings';
import { dataAuthHook } from './hook.data';

// useHistoryのMock化
const historyMock = jest.fn();
jest.mock('react-router-dom', () => ({
    useHistory: () => ({
        replace: historyMock
    })
}));


describe('認証フック', () => {

    describe('初回描画', () => {

        hookTest.getLoadingTest(dataAuthHook, dataAuthHook.successAPI)();
    });
    
    describe('認証処理', () => {

        asyncDomTest('認証に失敗するとログイン画面へ遷移すること', async (container) => {

            // GIVEN
            const testData = dataAuthHook;

            await apiTest('', async () => {

                // WHEN
                await act( async () => testData.initEvent(container)());

                // THEN
                expect(historyMock.mock.calls[0][0]).toBe(Setting.VIEW_PATH.LOGIN);

            }, [testData.failureAPI], true);
        }, false);
    });
});