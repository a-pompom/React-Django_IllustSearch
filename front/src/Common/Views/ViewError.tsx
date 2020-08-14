import React from 'react';
import * as BaseData from '../BaseData';

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