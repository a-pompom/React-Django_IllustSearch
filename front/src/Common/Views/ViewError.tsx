import React from 'react';
import * as BaseData from '../BaseData';

/**
 * 入力要素と結びつくエラーメッセージを表示するためのコンポーネント
 * 
 * @param errors エラーメッセージを格納したリスト
 */
export const Error: React.FC<BaseData.ErrorProps> = ({
    errors
}) => {

    return (
        <React.Fragment>
            {
                errors.map((error) => {
                    return (
                        <span className="Error" key={error}>{error}</span>
                    )
                })
            }
        </React.Fragment>
    )
};