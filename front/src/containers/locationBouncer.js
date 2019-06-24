import React from 'react'

import { Requesting, Failed } from '../components/locationBouncer'

import * as defs from '../defs'

export const withLocationBouncer = (Component) => {
    return class extends React.Component {
        render() {
            const locationStatus = this.props.locationStatus
            const locationError = this.props.locationError
            switch(locationStatus) {
                case defs.STATUS.REQUESTING:
                    return <Requesting />
                case defs.STATUS.FAILED:
                    return <Failed error={locationError}/>
                case defs.STATUS.SUCCESS:
                    return <Component {...this.props}/>
                default:
                    return ""
            }
        }
    }
}