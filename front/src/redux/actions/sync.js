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

export const userLocationRequested = utils.makeCreators(defs.USER_LOCATION_REQUESTED)
export const userLocationSuccess = utils.makeCreators(defs.USER_LOCATION_SUCCESS, "latitude", "longitude")
export const userLocationFailed = utils.makeCreators(defs.USER_LOCATION_FAILED, "error")

// --> PLACES
export const fetchNearbyRequested = utils.makeCreators(defs.FETCH_NEARBY_REQUESTED)
export const fetchNearbySuccess = utils.makeCreators(defs.FETCH_NEARBY_SUCCESS, "place_ids")
export const fetchNearbyFailed = utils.makeCreators(defs.FETCH_NEARBY_FAILED)

// -> GENERIC ADD ENTITIES
export const addEntities = utils.makeCreators(defs.ADD_ENTITIES, "entities")