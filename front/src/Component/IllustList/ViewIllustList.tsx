import React from 'react';

import { PhaseView } from 'Common/Views/ViewPhase';

import { useIllustList } from './useIllustList';
import * as IllustData from './illustListData';


export const IllustListView: React.FC<IllustData.Hook> = ({
    state
}) => {
    return (
        <React.Fragment>
            <div className="Top">

                <PhaseView
                    phase={state.phase.currentPhase}
                    message={state.phase.message}
                />
                <main className="IllustArea">

                    <ul className="IllustList">
                        {state.illust_list.map((illust) => (
                            <li
                                className="IllustList__item"
                                key={illust.path}
                            >
                                <a href="#">
                                    <img src={illust.path} className="Thumbnail"/>
                                </a>
                            </li>
                        ))}
                    </ul>

                </main>
            </div>

        </React.Fragment>
    );
};

export const IllustList = () => {

    const hook = useIllustList();

    return (
        <IllustListView {...hook} />
    );
};