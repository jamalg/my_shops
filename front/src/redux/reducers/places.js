import { fromJS } from 'immutable'
import * as defs from '../../defs'

export default function places(state=fromJS({}), action) {
    switch(action.type) {
        case defs.ADD_ENTITIES:
            return state.mergeWith((o,n) => o.merge(n) ,fromJS(action.payload.entities.places))
        default:
            return state
    }
}