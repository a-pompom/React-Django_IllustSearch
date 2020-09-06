
import * as BaseData from 'Common/BaseData';
import { Field } from 'Common/Field';

// APIからのレスポンス
export interface GetResponse extends BaseData.BaseAPIResponse {
    name: string,
    age: number
}
export interface PostResponse extends BaseData.BaseAPIResponse {}

// APIパラメータ
export interface GetAPIParam {
    name: string,
    age: number
}
export interface PostAPIBody {
    productName: string,
    price: number
}

export interface State extends BaseData.BaseState {}

// フィールド
export type FieldName = 'name' | 'age';
export type Value = string | number;
export type nameField<nameFieldName extends FieldName, nameValue extends Value> = Field<nameFieldName, nameValue>
export type ageField<ageFieldName extends FieldName, ageValue extends Value> = Field<ageFieldName, ageValue>

export interface ValidatorState extends BaseData.BaseState {
    name: nameField<'name', string>,
    age: ageField<'age', number>,
    isValid: boolean
}

export interface GetState extends BaseData.BaseState {
    actionHisotryList: string[],
    response: GetResponse
}
export interface PostState extends BaseData.BaseState {
    actionHisotryList: string[],
    response: PostResponse
}

// Action
interface ChildAction extends BaseData.BaseAction<'CHILD_ACTION'> {
}

interface GetSuccessHandlerAction extends BaseData.BaseAction<'GET_SUCCESS_HANDLER'>{ payload: {response: GetResponse }}
interface GetFailureHandlerAction extends BaseData.BaseAction<'GET_FAILURE_HANDLER'>{ payload: {response: GetResponse }}
interface PostSuccessHandlerAction extends BaseData.BaseAction<'POST_SUCCESS_HANDLER'>{ payload: {response: PostResponse }}
interface PostFailureHandlerAction extends BaseData.BaseAction<'POST_FAILURE_HANDLER'>{ payload: {response: PostResponse }}

export type IAction = BaseData.IBaseAction | ChildAction | GetSuccessHandlerAction | GetFailureHandlerAction | PostSuccessHandlerAction | PostFailureHandlerAction;

export interface ViewTestForReducerProps {
    argState: State,
    argAction: IAction,
    reducer: {(state: State, action: IAction): State}
};

export interface ViewTestForValidatorProps {
    argState: ValidatorState,
    fieldNames: FieldName[],
    fieldValues: Value[]
}

export interface ViewTestForGetAPIProps {
    argState: GetState,
    getPath: string,
    getParam: GetAPIParam,
    getAPI?: BaseData.GetAPI<GetAPIParam, GetResponse>
}
export interface ViewTestForPostAPIProps {
    argState: PostState,
    postPath: string,
    postBody: PostAPIBody,
    postAPI?: BaseData.PostAPI<PostAPIBody, BaseData.BaseAPIResponse>
}