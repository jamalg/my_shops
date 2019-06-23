import * as defs from '../../defs'
import * as utils from './utils'

// --> LOGIN
export const userLoginRequested = utils.makeCreators(defs.USER_LOGIN_REQUESTED)
export const userLoginSuccess = utils.makeCreators(defs.USER_LOGIN_SUCCESS, "accessToken")
export const userLoginFailed = utils.makeCreators(defs.USER_LOGIN_FAILED, "error")

// --> LOGOUT
export const userLogout = utils.makeCreators(defs.USER_LOGOUT)

// --> GENERAL USER MANAGEMENT
export const addUserRequested = utils.makeCreators(defs.ADD_USER_REQUESTED)
export const addUserSuccess = utils.makeCreators(defs.ADD_USER_SUCCESS, "userId")
export const addUserFailed = utils.makeCreators(defs.ADD_USER_FAILED, "error")

// -> GENERIC ADD ENTITIES
export const addEntities = utils.makeCreators(defs.ADD_ENTITIES, "entities")