import { fromJS, Set } from 'immutable'
import * as defs from '../../defs'

export default function currentUser(state=fromJS({}), action) {
    switch(action.type) {

        // LOGIN
        case defs.USER_LOGIN_REQUESTED:
            return state.withMutations(s =>
                s.set("isLogged", false)
                .set("loginStatus", defs.STATUS.REQUESTING)
                .delete("loginError")
            )
        case defs.USER_LOGIN_SUCCESS:
            return state.withMutations(s =>
                s.set("isLogged", true)
                .set("loginStatus", defs.STATUS.SUCCESS)
                .delete("loginError")
            )
        case defs.USER_LOGIN_FAILED:
            return state.withMutations(s =>
                s.set("loginStatus", defs.STATUS.FAILED)
                .set("isLogged", false)
                .set("loginError", action.payload.error)
                )

        // LOGOUT
        case defs.USER_LOGOUT:
            return state.withMutations(s =>
                s.set("isLogged", false)
                .delete("loginStatus")
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
                 .set("nearbyPlacesIds", Set(action.payload.place_ids))
            )
        case defs.FETCH_NEARBY_FAILED:
            return state.withMutations(s =>
                s.set("nearbyStatus", defs.STATUS.FAILED)
                .set("nearbyError", action.payload.error)
            )

        // SOCIAL
        case defs.ADD_LIKE_REQUESTED:
            return state.set("addLikeStatus", defs.STATUS.REQUESTING)
        case defs.ADD_LIKE_SUCCESS:
            return state.withMutations(s =>
                s.set("addLikeStatus", defs.STATUS.SUCCESS)
                 .removeIn(["nearbyPlacesIds", action.payload.place_id])
            )
        case defs.ADD_LIKE_FAILED:
            return state.withMutations(s =>
                s.set("addLikeStatus", defs.STATUS.FAILED)
                .set("addLikeError", action.payload.error)
            )

        case defs.ADD_DISLIKE_REQUESTED:
            return state.set("addDisLikeStatus", defs.STATUS.REQUESTING)
        case defs.ADD_DISLIKE_SUCCESS:
            return state.withMutations(s =>
                s.set("addDisLikeStatus", defs.STATUS.SUCCESS)
                 .removeIn(["nearbyPlacesIds", action.payload.place_id])
            )
        case defs.ADD_DISLIKE_FAILED:
            return state.withMutations(s =>
                s.set("addDisLikeStatus", defs.STATUS.FAILED)
                .set("addDisLikeError", action.payload.error)
            )

        default:
            return state
    }
}