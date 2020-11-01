import { useReducer, useEffect } from 'react';

import * as BaseHook from 'Common/useBase';
import { Setting } from 'settings';

import { handleIllustListGetSuccess } from './apiHandler';
import * as IllustData from './illustListData';
import { reducer } from './reducer';
import { Phase } from 'Common/Phase';

export const useIllustList = (): IllustData.Hook => {

    const initialState: IllustData.State = {
        illust_list: [],
        phase: new Phase('INIT'),
    };

    const reducerWrapper = BaseHook.useBaseReducer<IllustData.State, IllustData.IAction>(reducer);
    const [state, dispatch] = useReducer(reducerWrapper, initialState);

    const emitGet = BaseHook.useGetAPI<IllustData.GetResponse>(dispatch);

    useEffect(() => {

        emitGet(
            Setting.API_PATH.ILLUST.LIST,
            null,
            {
                handler: handleIllustListGetSuccess,
                args: [dispatch],
            }
        );

    }, []);

    return {
        state
    };

};