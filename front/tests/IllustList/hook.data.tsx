import React from 'react';
import { render } from 'react-dom';

import { Setting } from 'settings';
import * as IllustData from 'Component/IllustList/illustListData';
import { IllustList } from 'Component/IllustList/ViewIllustList';

import { getAPIInfo } from '../testUtils/testAPIUtils';
import * as TestData from './data';

/**
 * 初期描画用API・描画イベント
 */
const getInitial = () => {

    const successAPI = getAPIInfo<null, IllustData.GetResponse>(
        `${Setting.API_ENDPOINT}${Setting.API_PATH.ILLUST.LIST}`,
        'get',
        {
            body: {
                illust_list: TestData.simpleImageList
            },
            status: 200,
            ok: true,
        },
        null,
    );

    const initEvent = (container: HTMLElement) => {

        return () => {
            render(
                <IllustList />,
                container
            );
        };
    };

    const illustList = TestData.simpleImageList;

    return {
        successAPI,
        initEvent,
        illustList,
    };
};

export const initial = getInitial();