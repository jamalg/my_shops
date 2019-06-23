import { denormalize } from 'normalizr'
import * as schemas from './schemas'

export const getUserData = (state, userId) => denormalize(userId, schemas.user, state )

// LOGIN
export const isUserLogged = (state) => state.getIn(["currentUser", "isLogged"])
export const getLoggingStatus = (state) => state.getIn(["currentUser", "LoginStatus"])

// CURRENT USER DATA
export const getCurrentUserId = (state) => state.getIn(["currentUser", "id"])
export const getCurrentUserData = (state) => getUserData(state, getCurrentUserId(state))