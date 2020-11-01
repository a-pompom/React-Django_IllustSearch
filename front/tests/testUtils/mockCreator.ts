import React from 'react';

/**
 * React関連のモジュールをモック化
 */
const getReactMockCreator = () => {

    /**
     * useEffectレンダリング前の状態を取得するために、useEffectを空とする
     */
    const createEmptyUseEffectMock = () => {

        const useEffectMock = jest.spyOn(React, 'useEffect').mockImplementation((f) => {});
        return useEffectMock;
    };

    return {
        createEmptyUseEffectMock,
    };
};

export const reactMockCreator = getReactMockCreator();