import { act } from 'react-dom/test-utils';

import { asyncDomTest, apiTest } from '../testUtils/testDecorators';
import { hookTest } from '../testUtils/testForCommon';

import { initial } from './hook.data';

describe('イラスト一覧フック', () => {

    describe('初期描画', () => {

        hookTest.getLoadingTest(initial, initial.successAPI)();

        asyncDomTest('イラスト一覧APIでsrc属性を持つimg要素が描画されること', async (container) => {

            // GIVEN
            const testData = initial;

            await apiTest('', async () => {

                // WHEN
                await act( async () => testData.initEvent(container)());

                // THEN
                expect(document.querySelectorAll('.IllustList__item').length).not.toBe(0);
                document.querySelectorAll('.Thumbnail').forEach((item: HTMLImageElement, index) => {

                    expect(item.src).toContain(testData.illustList[index].path);
                });
            }, [testData.successAPI], true);
        }, false);
    });
});