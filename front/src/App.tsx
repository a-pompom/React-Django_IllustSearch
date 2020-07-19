import React from 'react';
import { BrowserRouter, Switch, Route } from 'react-router-dom';


const App = () =>{

    return (
        <BrowserRouter>
            <Switch>
                <Route path="/" children={<div></div>}></Route>
            </Switch>
        </BrowserRouter>
    );
}

export default App;