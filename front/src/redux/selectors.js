import { denormalize } from 'normalizr'

import * as schemas from './schemas'
import * as defs from '../defs'

export const getUserData = (state, userId) => denormalize(userId, schemas.user, state )

// LOGIN
export const isUserLogged = (state) => state.getIn(["currentUser", "isLogged"])
export const getLoggingStatus = (state) => state.getIn(["currentUser", "loginStatus"])

// CURRENT USER DATA
export const getCurrentUserId = (state) => state.getIn(["currentUser", "id"])
export const getCurrentUserData = (state) => getUserData(state, getCurrentUserId(state))
export const getLocationStatus = (state) => state.getIn(["currentUser", "locationStatus"])
export const getUserLocation = (state) => getLocationStatus(state) === defs.STATUS.SUCCESS &&
    {latitude: state.getIn(["currentUser", "latitude"]), longitude: state.getIn(["currentUser", "longitude"])}

// PLACES
export const getNearbyFetchStatus = (state) => state.getIn(["currentUser", "nearbyStatus"])
export const getNearbyPlaceIds = (state) => getNearbyFetchStatus(state) === defs.STATUS.SUCCESS && state.getIn(["currentUser", "nearbyPlacesIds"])
export const getNearbyPlaces = (state) => getNearbyPlaceIds(state) && getNearbyPlaceIds(state).map(placeId => state.getIn(["places", placeId.toString()]))
export const getLikedFetchStatus = (state) => state.getIn(["currentUser", "likedStatus"])
export const getLikedPlaceIds = (state) => getLikedFetchStatus(state) === defs.STATUS.SUCCESS && state.getIn(["currentUser", "likedPlacesIds"])
export const getLikedPlaces = (state) => getLikedPlaceIds(state) && getLikedPlaceIds(state).map(placeId => state.getIn(["places", placeId.toString()]))