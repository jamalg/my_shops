import fetch from 'cross-fetch'

import { toCamelCaseObject, toSnakeCaseObject } from './utils'


const applicationJSON = "application/json"
const backApi = process.env.REACT_APP_API_URL

const fetchBackApi = (endpoint, requestInit) => {
    return fetch(`${backApi}/${endpoint}`, requestInit)
    .then(response => {
        if ( parseInt(response.status / 100) !== 2) {
            if (response.headers.get("content-type") === applicationJSON) {
                return response.json()
                .then(json => {
                    throw toCamelCaseObject(json)
                })
            }
            const error = {message: response.statusText}
            throw error
        } else {
            if (response.headers.get("content-type") === applicationJSON) {
                return response.json()
                .then(json => toCamelCaseObject(json))
            }
            return response.statusText
        }
    })
}

const getBackApi = (endpoint) => fetchBackApi(endpoint)
const deleteBackApi = (endpoint) => fetchBackApi(endpoint, {method: 'DELETE'})
const postBackApi = (endpoint, payload) => fetchBackApi(
    endpoint,
    {
        headers: {
            'Content-Type': applicationJSON,
        },
        method: 'POST',
        body: JSON.stringify(toSnakeCaseObject(payload))
    }
)

// Login Register
export const logUser = (email, password) => postBackApi("auth/login", {email, password})
export const registerUser = (userData) => postBackApi("users", userData)

// General user management
export const addUser = (userData) => postBackApi("users", userData)

// Places
export const getNearby = (latitude, longitude) => getBackApi(`places/nearby?latitude=${latitude}&longitude=${longitude}`)
export const getLiked = () => getBackApi("places/liked")
export const addLike = (placeId) => postBackApi("me/likes", {placeId})
export const addDisLike = (placeId) => postBackApi("me/dislikes", {placeId})