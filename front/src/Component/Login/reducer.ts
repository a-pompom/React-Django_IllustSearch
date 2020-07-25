import { User, LoginState } from './loginData';

export type DispatchType = 'INIT' | 'LOGIN';

interface BaseAction {
    type: DispatchType
};

export interface InitAction extends BaseAction{
    type: 'INIT',
    payload: {
        users: User[]
    }
};

export interface LoginAction extends BaseAction{
    type: 'LOGIN',
    payload: {
        username: string
    }
};

type IAction = InitAction | LoginAction;

export const reducer = (state: LoginState, action: IAction): LoginState => {

    const modState = {...state};

    if (action.type === 'INIT'){
        console.log('reducer init');
        console.log(action.payload.users);

        modState.users = action.payload.users;
    }

    return modState;
};