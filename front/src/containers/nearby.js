import React from 'react'
import { connect } from 'react-redux'
import withImmutablePropsToJS from 'with-immutable-props-to-js'

import Nearby from '../components/nearby'
import { fetchNearby, fetchUserLocation } from '../redux/actions/async'
import { getNearbyPlaces, getNearbyFetchStatus, isUserLogged, getUserLocation, getLocationStatus } from '../redux/selectors'
import * as defs from '../defs'


class NearbyContainer extends React.Component {
    componentDidMount() {
        this.props.fetchUserLocation()
    }

    componentDidUpdate(prevProps) {
        const prevLocationStatus = prevProps.locationStatus
        const locationStatus = this.props.locationStatus
        if (prevLocationStatus == defs.STATUS.REQUESTING && locationStatus == defs.STATUS.SUCCESS ) {
            const {latitude, longitude} = this.props.userLocation
            this.props.fetchNearby(latitude, longitude)
        }
    }

    render() {
        return <Nearby
                    places={this.props.places}
                    status={this.props.status}
                    isLogged={this.props.isLogged}
                    locationStatus={this.props.locationStatus}
                    userLocation={this.props.userLocation}
                />
    }
}

const mapStateToProps = (state) => ({
    isLogged: isUserLogged(state),
    places: getNearbyPlaces(state),
    status: getNearbyFetchStatus(state),
    locationStatus: getLocationStatus(state),
    userLocation: getUserLocation(state),
})

const mapDispatchToProps = {
    fetchNearby,
    fetchUserLocation
}

export default connect(mapStateToProps, mapDispatchToProps)(withImmutablePropsToJS(NearbyContainer))
