import { combineReducers } from 'redux-immutable'
import currentUser from './currentUser'
import places from './places'

export default combineReducers({currentUser, places})
