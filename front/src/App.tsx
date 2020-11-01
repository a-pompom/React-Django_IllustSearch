import React from 'react';
import { HashRouter, Switch, Route, Redirect } from 'react-router-dom';

import { Setting } from 'settings';
import { Login } from 'Component/Login/ViewLogin';
import { Signup } from 'Component/Signup/viewSignup';

import { LoginRequired } from 'Component/Auth/ViewLoginRequiredRoute';
import { IllustList } from 'Component/IllustList/ViewIllustList';

const App = () =>{

    return (
        <HashRouter>
            <Switch>
                <Route exact path="/" children={<Login />}></Route>
                <Route exact path={Setting.VIEW_PATH.SIGNUP} children={<Signup />}></Route>
                <LoginRequired>
                    <Switch>
                        <Route exact path={Setting.VIEW_PATH.TOP} children={<IllustList />}></Route>
                        <Redirect from='*' to='/' />
                    </Switch>
                </LoginRequired>
            </Switch>
        </HashRouter>
    );
}

export default App;