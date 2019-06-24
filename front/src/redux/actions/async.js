import { normalize } from 'normalizr'
import * as schemas from '../schemas'

import * as sync from './sync'
import * as api from '../../api'
import * as defs from '../../defs'

export function fetchUserLocation() {
    return (dispatch) => {
        dispatch(sync.userLocationRequested())
        if (!navigator.geolocation) dispatch(sync.userLocationFailed("Geolocalisation is not supported by your browser"))
        navigator.geolocation.getCurrentPosition(
            (position) => dispatch(sync.userLocationSuccess(position.coords.latitude, position.coords.longitude)),
            (error) => dispatch(sync.userLoginFailed(error.message))
        )
    }
}


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

export function fetchNearby(latitude, longitude) {
    return (dispatch) => {
        dispatch(sync.fetchNearbyRequested())
        api.getNearby(latitude, longitude)
        .then(
            (places) => {
                const data = normalize(places, [ schemas.place ] )

                dispatch(sync.addEntities(data.entities))
                dispatch(sync.fetchNearbySuccess(places.map(place => place.id)))
            },
            (error) => dispatch(sync.fetchNearbyFailed(error.message))
        )
        }
}

export function fetchLiked() {
    return (dispatch) => {
        dispatch(sync.fetchLikedRequested())
        api.getLiked()
        .then(
            (places) => {
                const data = normalize(places, [ schemas.place ] )

                dispatch(sync.addEntities(data.entities))
                dispatch(sync.fetchLikedSuccess(places.map(place => place.id)))
            },
            (error) => dispatch(sync.fetchLikedFailed(error.message))
        )
        }
}

export function addLike(placeId) {
    return (dispatch) => {
        dispatch(sync.addLikeRequested())
        api.addLike(placeId)
        .then(
            (likeData) => {
                dispatch(sync.addLikeSuccess(placeId, likeData.id))
                return {status: defs.STATUS.SUCCESS}
            },
            (error) => {
                dispatch(sync.addLikeFailed(error.message))
                return {status: defs.STATUS.FAILED, errors: error.message}
            }
        )
        }
}

export function addDisLike(placeId) {
    return (dispatch) => {
        dispatch(sync.addDisLikeRequested())
        api.addDisLike(placeId)
        .then(
            () => {
                dispatch(sync.addDisLikeSuccess(placeId))
                return {status: defs.STATUS.SUCCESS}
            },
            (error) => {
                dispatch(sync.addDisLikeFailed(error.message))
                return {status: defs.STATUS.FAILED, errors: error.message}
            }
        )
        }
}