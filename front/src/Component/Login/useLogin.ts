import React, { useReducer, useEffect } from 'react';

import { LoginState, LoginHook} from './loginData';
import { reducer, InitAction, LoginAction } from './reducer';
import { getUserList } from './apiHandler';

export const useLogin = () => {

    useEffect(() => {

        const fetchData = async() => {

            const response = await getUserList()

            const action: InitAction = {
                type: 'INIT',
                payload: {
                    users: response,
                }
            }

            dispatch(action);

        };

        fetchData();

    }, []);

    const initialState: LoginState = {
        users: [],
        loginUsername: ''
    }

    const [state, dispatch] = useReducer(reducer, initialState);

    return {
        state: state
    };

};