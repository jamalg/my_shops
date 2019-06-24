import { fromJS } from 'immutable'
import * as defs from '../../defs'

export default function currentUser(state=fromJS({}), action) {
    switch(action.type) {

        // LOGIN
        case defs.USER_LOGIN_REQUESTED:
            return state.withMutations(s =>
                s.set("isLogged", false)
                .set("LoginStatus", defs.STATUS.REQUESTING)
                .delete("error")
            )
        case defs.USER_LOGIN_SUCCESS:
            window.localStorage.setItem("accessToken", action.payload.accessToken)
            return state.withMutations(s =>
                s.set("isLogged", true)
                .set("LoginStatus", defs.STATUS.SUCCESS)
                .delete("loginError")
            )
        case defs.USER_LOGIN_FAILED:
            return state.withMutations(s =>
                s.set("LoginStatus", defs.STATUS.FAILED)
                .set("isLogged", false)
                .set("loginError", action.payload.error)
                )

        // LOGOUT
        case defs.USER_LOGOUT:
            window.localStorage.removeItem("accessToken")
            return state.withMutations(s =>
                s.set("isLogged", false)
                .delete("LoginStatus")
                .delete("logoutError")
            )

        // USER LOCATION
        case defs.USER_LOCATION_REQUESTED:
            return state.withMutations(s =>
                s.set("locationStatus", defs.STATUS.REQUESTING)
                .delete("latitude")
                .delete("longitude")
                .delete("locationError")
            )
        case defs.USER_LOCATION_SUCCESS:
            return state.withMutations(s =>
                s.set("locationStatus", defs.STATUS.SUCCESS)
                .set("latitude", action.payload.latitude)
                .set("longitude", action.payload.longitude)
                .delete("locationError")
            )
        case defs.USER_LOCATION_FAILED:
            return state.withMutations(s =>
                s.set("locationStatus", defs.STATUS.FAILED)
                .set("locationError", action.payload.error)
                .delete("latitude")
                .delete("longitude")
            )

        // USER NEARBY PLACES
        case defs.FETCH_NEARBY_REQUESTED:
            return state.set("nearbyStatus", defs.STATUS.REQUESTING)
        case defs.FETCH_NEARBY_SUCCESS:
            return state.withMutations(s =>
                s.set("nearbyStatus", defs.STATUS.SUCCESS)
                 .set("nearbyPlacesIds", fromJS(action.payload.place_ids))
            )
        case defs.FETCH_NEARBY_FAILED:
            return state.withMutations(s =>
                s.set("nearbyStatus", defs.STATUS.FAILED)
                .set("nearbyError", action.payload.error)
            )
        default:
            return state
    }
}