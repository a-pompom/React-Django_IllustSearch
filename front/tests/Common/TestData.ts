
import * as BaseData from 'Common/BaseData';
import { Field } from 'Common/Field';

// APIからのレスポンス
export type GetResponse = BaseData.BaseAPIResponse & {
    body: BaseData.BaseAPIResponse['body'] & {
        name: string,
        age: number

    }
};
export type PostResponse = BaseData.BaseAPIResponse & {};

// APIパラメータ
export type GetAPIParam  ={
    name: string,
    age: number
};
export type PostAPIBody = {
    productName: string,
    price: number
};

export type State = BaseData.BaseState & {};

// フィールド
export type FieldName = 'name' | 'age';
export type Value = string | number;
export type nameField<nameFieldName = FieldName, nameValue = Value> = Field<nameFieldName, nameValue>
export type ageField<ageFieldName = FieldName, ageValue = Value> = Field<ageFieldName, ageValue>

export type ValidatorState = BaseData.BaseState & {
    name: nameField<'name', string>,
    age: ageField<'age', number>,
    isValid: boolean
};

export type GetState = BaseData.BaseState & {
    actionHisotryList: string[],
    response: GetResponse
};
export type PostState = BaseData.BaseState & {
    actionHisotryList: string[],
    response: PostResponse
};

// Action
type ChildAction = BaseData.BaseAction<'CHILD_ACTION'> & {
};

type GetSuccessHandlerAction = BaseData.BaseAction<'GET_SUCCESS_HANDLER'> & { payload: {response: GetResponse }};
type GetFailureHandlerAction = BaseData.BaseAction<'GET_FAILURE_HANDLER'> & { payload: {response: GetResponse }}
type PostSuccessHandlerAction = BaseData.BaseAction<'POST_SUCCESS_HANDLER'> & { payload: {response: PostResponse }};
type PostFailureHandlerAction = BaseData.BaseAction<'POST_FAILURE_HANDLER'> & { payload: {response: PostResponse }};

export type IAction = BaseData.IBaseAction | ChildAction | GetSuccessHandlerAction | GetFailureHandlerAction | PostSuccessHandlerAction | PostFailureHandlerAction;

export type ViewTestForReducerProps = {
    argState: State,
    argAction: IAction,
    reducer: {(state: State, action: IAction): State}
};

export type ViewTestForValidatorProps = {
    argState: ValidatorState,
    fieldNames: FieldName[],
    fieldValues: Value[]
};

export type ViewTestForGetAPIProps = {
    argState: GetState,
    getPath: string,
    getParam: GetAPIParam,
    getAPI?: BaseData.GetAPI<GetAPIParam, GetResponse>
};
export type ViewTestForPostAPIProps = {
    argState: PostState,
    postPath: string,
    postBody: PostAPIBody,
    postAPI?: BaseData.PostAPI<PostAPIBody, BaseData.BaseAPIResponse>
};