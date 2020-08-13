import { Phase as PhaseClass } from './Phase';

// API

type StatusOK = 200
type StatusRedirect = 301 | 302 | 303
type StatusClientError = 400 | 401 | 403 | 404 | 405
type StatusServerError = 500
export type StatusCode = StatusOK | StatusRedirect | StatusClientError | StatusServerError

// APIレスポンスのエラー内容
export interface ErrorObject {
    fieldName: string,
    message: string
}

export interface BaseGetResponse {
    statusCode: StatusCode,
    ok: boolean,
    errors?: ErrorObject[]
}

// POSTレスポンス メッセージとステータスコードを格納
export interface PostResponse {
    message: string,
    statusCode: StatusCode,
    ok: boolean,
    errors?: ErrorObject[]
}
// APIへのGETリクエスト関数
export type GetAPI<GetParameter, GetResponse> = {(param?: GetParameter): Promise<GetResponse>}

export interface GetCallbackHandler<Args extends any[]> {
    handler: {(response: BaseGetResponse, ...args : Args)},
    args: Args
}

// APIへのPOSリクエスト関数
export type PostAPI<Body> = {(body: Body): Promise<PostResponse>}

export interface PostCallbackHandler<Args extends any[]> {
    handler: {(...args : Args)},
    args: Args
}

// 画面上の処理の進行状況
export type Phase = 'INIT' | 'IDLE' | 'LOADING' | 'FAILURE' | 'FATAL'
// 進行状況用コンポーネントのProp
export interface PhaseProps {
    phase: Phase,
    message?: string
}

// アクション

// 基底アクション
export interface BaseAction<DispatchType> {
    type: DispatchType
};


// 処理待機中アクション ユーザからのイベントを待機している状態
export interface IdleAction extends BaseAction<'IDLE'> {}

export interface BeforeGetAction extends BaseAction<'BEFORE_GET'>{}

export interface AfterGetAction extends BaseAction<'SUCCESS_GET'| 'FAILURE_GET'> {
    payload: {
        response: BaseGetResponse
    }
}

// POST前処理アクション 二重POSTを防止するため、処理フェーズを切り替える
export interface BeforePostAction extends BaseAction<'BEFORE_POST'>{}
// POST後処理アクション 処理結果に応じてアクションの種類を切り替え
export interface AfterPostAction extends BaseAction<'SUCCESS_POST' | 'FAILURE_POST'>{
    payload: {
        response: PostResponse
    }
}

// ディレイタイマー追加アクション 各Phaseでディレイ表示が必要な要素を管理するために利用
export interface AddTimerAction extends BaseAction<'ADD_TIMER'> {
    payload: {
        timer: NodeJS.Timeout
    }
}

// アクションインタフェース
export type IBaseAction = IdleAction | BeforeGetAction | AfterGetAction |  BeforePostAction | AfterPostAction | AddTimerAction
export const I_BASE_ACTIONS = ['IDLE', 'BEFORE_GET', 'SUCCESS_GET', 'FAILURE_GET', 'BEFORE_POST', 'SUCCESS_POST', 'FAILURE_POST', 'ADD_TIMER'];
    
// State 

export interface BaseState {
    phase: PhaseClass
}
// HTMLの入力フィールドの値がとりうる型
export type BaseValue = string;