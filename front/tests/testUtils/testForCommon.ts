import { act } from 'react-dom/test-utils';
import { asyncDomTest, apiTest } from '../testUtils/testDecorators';
import { reactMockCreator } from '../testUtils/mockCreator';

type TestData = {
    initEvent: (container: HTMLElement) => () => void;
};

/**
 * 初回読み込みでLoadingが表示されるか検証
 * 
 * @param testData 初期描画イベントを持つテストデータ
 * @param api モックAPI
 */
const getLoadingTest = (testData: TestData, api: any) => {

    return () => {
        asyncDomTest('初期描画では読み込み中となること', async (container) => {

            // GIVEN
            // 初回のレンダリング結果を検証するため、useEffectを無効化
            const mockCreator = reactMockCreator;
            const mock = mockCreator.createEmptyUseEffectMock();

            await apiTest('', async () => {

                // WHEN
                await act( async () => testData.initEvent(container)());

                // THEN
                expect(document.querySelector('.Loading')).not.toBeNull();

                mock.mockRestore();
            }, [api], true);
        }, false);
    };
};

export const hookTest = {
    getLoadingTest
};