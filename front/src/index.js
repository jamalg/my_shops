import 'babel-polyfill'

import React from 'react'
import ReactDom from 'react-dom'
import { BrowserRouter as Router } from 'react-router-dom'
import { Provider } from 'react-redux'
import { fromJS } from 'immutable'

import App from './App'
import configureStore from './redux/store'
import './index.css'
import * as serviceWorker from './serviceWorker';

if (process.env.REACT_APP_ENVIRONMENT && process.env.REACT_APP_ENVIRONMENT !== "production") {
    require("immutable-devtools")(require("immutable"))
}

const initialState = fromJS({
    currentUser: {}
})
const store = configureStore(initialState)

ReactDom.render(
    <Provider store={store}>
        <Router>
            <App/>
        </Router>
    </Provider>,
    document.getElementById("root")
)

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
