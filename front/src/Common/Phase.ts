import * as BaseData from './BaseData';

/**
 * 読み込み中や失敗など、処理の進行状況を管理するためのクラス
 */
export class Phase {

    // 現在の処理状況 初期処理・読み込み中など
    public currentPhase: BaseData.Phase;
    // 状況を表すメッセージ エラー内容や処理完了など
    public message: string;

    // 設定中のタイマーのリスト 各Phaseでフェードアウトのようにコンポーネントを表示する際、
    // ユーザの操作により、タイマー通りに表示すると不自然になることがある(ex: エラーメッセージフェードアウト中に再度submit)
    // Phaseごとにタイマーも初期化するため、アクティブなものをリストで管理
    private _activeTimers: NodeJS.Timeout[];

    constructor(initialPhase: BaseData.Phase, message?: string) {
        this.currentPhase = initialPhase;
        this._activeTimers = [];

        this.message = message;
    }

    /**
     * 現在有効なタイマー要素を追加
     * 
     * @param timerId 追加対象のタイマーID
     */
    public addActiveTimer(timer: NodeJS.Timeout) {

        this._activeTimers.push(timer);
    }

    /**
     * Phaseを変更した際、前の処理でアクティブだったタイマーを消去
     * これにより、ボタン連打等で複数回処理が実行されても、タイマーが蓄積されることを防ぐ
     */
    public initialize() {
        this.message = '';

        this._activeTimers.forEach((timer) => {

            clearTimeout(timer);
        });

        this._activeTimers = [];
    }
}