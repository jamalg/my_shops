import { normalize } from 'normalizr'
import * as schemas from '../schemas'

import * as sync from './sync'
import * as api from '../../api'
import * as defs from '../../defs'

export function logUser(userId, password) {
    return (dispatch) => {
        dispatch(sync.userLoginRequested(userId))
        api.logUser(userId, password)
        .then(
            ({ accessToken }) => dispatch(sync.userLoginSuccess(accessToken)),
            (error) => dispatch(sync.userLoginFailed(error.message))
        )
    }
}

export function addUser(userData) {
    return (dispatch) => {
        dispatch(sync.addUserRequested())
        api.addUser(userData)
        .then(
            (userData) => {
                const data = normalize(userData, schemas.user)

                dispatch(sync.addEntities(data.entities))
                dispatch(sync.addUserSuccess(userData.id))
                return {status: defs.STATUS.SUCCESS}
            },
            (error) => {
                dispatch(sync.addUserFailed(error.message))
                return {status: defs.STATUS.FAILED, errors: error.message}
            }
        )
        }
}
