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

        default:
            return state
    }
}