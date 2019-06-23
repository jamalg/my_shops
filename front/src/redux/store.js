import {createStore, compose, applyMiddleware} from 'redux'
import ThunkMiddleware from 'redux-thunk'
import LoggerMiddleware from 'redux-logger'
import rootReducer from './reducers/rootReducer'

export default function(initialState) {

    const middlewares = [ThunkMiddleware]
    if (process.env.REACT_APP_ENVIRONMENT !== "production") middlewares.push(LoggerMiddleware)
    const middlewareEnhancer = applyMiddleware(...middlewares)

    const enhancers = [middlewareEnhancer]
    if (process.env.REACT_APP_ENVIRONMENT !== "production") enhancers.push(window.__REDUX_DEVTOOLS_EXTENSION__ && window.__REDUX_DEVTOOLS_EXTENSION__())

    return createStore(rootReducer, initialState, compose(...enhancers))
}