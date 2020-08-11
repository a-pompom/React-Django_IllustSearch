import React from 'react';
import * as BaseData from './BaseData';

/**
 * 読込中や登録完了など、処理の進行状況に応じたViewを表示するためのコンポーネント
 * 
 * @param phase 処理状況
 */
export const PhaseView: (React.FC<BaseData.PhaseProps>) = ({
    phase,
    message
}) => {

    // 通常表示 何もしない
    if (phase === 'IDLE') {
        return null;
    }

    // 読込中 二重POSTなど予期しない動作を防ぐためにオーバーレイを表示
    if (phase === 'LOADING' || phase === 'INIT') {

        return (
            <React.Fragment>
                <div className="Loading"></div>
                <div className="LoadingOverlay"></div>
            </React.Fragment>
        )
    }

    // 処理失敗 ユーザへメッセージを表示
    if (phase === 'FAILURE') {

        return (
            <div className="PopupError">{message}</div>
        )
    }

};