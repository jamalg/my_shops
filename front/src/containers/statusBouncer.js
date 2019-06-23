import React from 'react'

import { Requesting, Failed } from '../components/statusBouncer'

import * as defs from '../defs'

export const withStatusBouncer = (Component) => {
    return class extends React.Component {
        render() {
            const status = this.props.status
            switch(status) {
                case defs.STATUS.REQUESTING:
                    return <Requesting />
                case defs.STATUS.FAILED:
                    return <Failed />
                case defs.STATUS.SUCCESS:
                    return <Component {...this.props} />
                default:
                    return ""
            }
        }
    }
}