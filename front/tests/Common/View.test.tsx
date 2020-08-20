import React from 'react';
import { render } from 'react-dom';
import { act } from 'react-dom/test-utils';

import { domTest, domTestEach } from '../testUtils/testDecorators';

import { Phase } from 'Common/Phase';
import { Error } from 'Common/Views/ViewError';
import { PhaseView } from 'Common/Views/ViewPhase';


describe('汎用Viewの表示検証', () => {

    describe('ErrorメッセージView', () => {

        const classSelector = '.Error';
        const expectedTagName = 'SPAN';

        domTest('コンポーネントが表示されること。', (container: HTMLDivElement) => {

            // GIVEN
            const errorMessage = 'そのユーザ名は既に使用されています。';

            // WHEN
            // コンポーネントの描画
            act(() => {
                render(<Error errors={[errorMessage]} />, container);
            })

            const actual = document.querySelector(classSelector);

            // THEN
            expect(actual.textContent).toBe(errorMessage);
            expect(actual.tagName).toBe(expectedTagName);
        });

        domTest('複数のエラーメッセージがspan要素で描画されること。', (container: HTMLDivElement) => {

            // GIVEN
            const errors = [
                'ユーザ名は10文字以上で入力してください。',
                'ユーザ名には半角英数と-_のみ利用できます。',
                'そのユーザ名は既に使用されています。'
            ];

            // WHEN
            // コンポーネントの描画
            act(() => {
                render(<Error errors={errors} />, container);
            })

            const actual = document.querySelectorAll(classSelector);

            // THEN
            expect(actual.length).toBe(errors.length);
            expect(actual[0].tagName).toBe(expectedTagName);

            // エラーメッセージ 検証
            actual.forEach((errorDOM, index) => {

                expect(errorDOM.textContent).toBe(errors[index]);
            });
        });
    });

    describe('処理進行状況View', () => {


        domTest('PhaseがIDLE状態のときは、何も表示されないこと。', (container: HTMLDivElement) => {

            // GIVEN
            const phase = new Phase('IDLE');

            // WHEN
            act(() => {
                render(<PhaseView phase={phase.currentPhase} />, container);
            });

            // THEN
            expect(container.childNodes.length).toBe(0);
        });

        domTest('PhaseがFAILURE状態のときは、ポップアップエラーメッセージが表示されること。', (container: HTMLDivElement) => {

            // GIVEN
            const errorMessage = 'ユーザ登録に失敗しました。';
            const expectedClassSelector = '.PopupError';

            const phase = new Phase('FAILURE', errorMessage);

            // WHEN
            act(() => {
                render(<PhaseView phase={phase.currentPhase} message={phase.message} />, container);
            });
            const actual = document.querySelector(expectedClassSelector);

            // THEN
            expect(actual.textContent).toBe(errorMessage);
        });

        type LoadingTestArgs = [string, Phase];

        domTestEach<LoadingTestArgs>([
            ['INIT', new Phase('INIT')],
            ['LOADING', new Phase('LOADING')]
        ], '読み込み処理中に読み込み中オーバーレイが表示されること。_%s', (_, phase: Phase, container: HTMLDivElement) => {

            // GIVEN
            const expectedLoadingClassSelector = '.Loading';
            const expectedOverlayClassSelector = '.LoadingOverlay';

            // WHEN
            act(() => {
                render(<PhaseView phase={phase.currentPhase} />, container);
            });
            const actualLoading = document.querySelector(expectedLoadingClassSelector);
            const actualOverlay = document.querySelector(expectedOverlayClassSelector)

            // THEN
            expect(actualLoading).not.toBe(null);
            expect(actualOverlay).not.toBe(null);
        });

    });
});