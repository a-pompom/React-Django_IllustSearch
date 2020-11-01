import { Phase as PhaseClass } from './Phase';

// API
type StatusOK = 200
type StatusRedirect = 301 | 302 | 303
type StatusClientError = 400 | 401 | 403 | 404 | 405 | 422
type StatusServerError = 500
export type StatusCode = StatusOK | StatusRedirect | StatusClientError | StatusServerError

// APIレスポンスのエラー内容
export type ErrorObject = {
    fieldName: string,
    message: string
};

export type BaseAPIResponse = {
    body: {
        message?: string,
        errors?: ErrorObject[]
    },
    status: StatusCode,
    ok: boolean,
};


// GET API
export type GetAPI<GetParameter extends {}, GetResponse extends BaseAPIResponse> = {(path: string, param?: GetParameter): Promise<GetResponse>};

export type GetCallbackHandler<Response extends BaseAPIResponse, Args extends any[]> = {
    handler: {(response: Response, ...args : Args)},
    args: Args
};

// POST API
export type PostAPI<Body, PostResponse extends BaseAPIResponse> = {(path: string, body: Body): Promise<PostResponse>};

export type PostCallbackHandler<Args extends any[]> = {
    handler: {(response: BaseAPIResponse, ...args : Args)},
    args: Args
};


// 画面上の処理の進行状況
export type Phase = 'INIT' | 'IDLE' | 'LOADING' | 'FAILURE' | 'FATAL';
// 進行状況用コンポーネントのProp
export type PhaseProps = {
    phase: Phase,
    message?: string
};

// アクション

// 基底アクション
export type BaseAction<DispatchType> = {
    type: DispatchType
};

// 処理待機中アクション ユーザからのイベントを待機している状態
export type IdleAction = BaseAction<'IDLE'> & {};

// GET前後処理アクション
export type BeforeGetAction = BaseAction<'BEFORE_GET'> & {};
export type AfterGetAction = BaseAction<'SUCCESS_GET'| 'FAILURE_GET'> & {
    payload: {
        response: BaseAPIResponse
    }
}

// POST前処理アクション 二重POSTを防止するため、処理フェーズを切り替える
export type BeforePostAction = BaseAction<'BEFORE_POST'> & {};
// POST後処理アクション 処理結果に応じてアクションの種類を切り替え
export type AfterPostAction = BaseAction<'SUCCESS_POST' | 'FAILURE_POST'> & {
    payload: {
        response: BaseAPIResponse
    }
};

// バリデーション後処理アクション ユーザの入力値やエラーメッセージをStateへ反映
export type AfterValidationAction<FieldNames, Values> = BaseAction<'AFTER_VALIDATION'> & {
    payload: {
        results: ValidationResult<FieldNames, Values>[]
    }
}
// バリデーション結果 ネストしたフィールド要素も更新できるよう、name要素・値・エラーを個別に保持
export type ValidationResult<FieldName, Value> = {
    isValid: boolean,
    fieldName: FieldName,
    fieldValue: Value
    errors: string[]
};

// ディレイタイマー追加アクション 各Phaseでディレイ表示が必要な要素を管理するために利用
export type AddTimerAction = BaseAction<'ADD_TIMER'> & {
    payload: {
        timer: NodeJS.Timeout
    }
};

// アクションインタフェース
export type IBaseAction = 
    IdleAction | 
    AfterValidationAction<string, unknown> | 
    BeforeGetAction | AfterGetAction |  BeforePostAction | AfterPostAction | 
    AddTimerAction
export const I_BASE_ACTIONS = ['IDLE', 'AFTER_VALIDATION', 'BEFORE_GET', 'SUCCESS_GET', 'FAILURE_GET', 'BEFORE_POST', 'SUCCESS_POST', 'FAILURE_POST', 'ADD_TIMER'];
    
// State 

export type BaseState = {
    phase: PhaseClass
};

// エラーメッセージ表示用コンポーネント
export type ErrorProps = {
    errors: string[]
};