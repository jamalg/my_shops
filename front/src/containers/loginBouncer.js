import React from 'react'
import { Redirect } from 'react-router-dom'

import LoginBouncer from '../components/loginBouncer'


export const withLoginBouncer = (Component) => {
    return class extends React.Component {
        constructor(props) {
            super(props)
            this.state = {
                redirect: false
            }
        }

        componentDidMount() {
            setTimeout(() => this.setState({redirect: true}), 2000)
        }

        render() {
            const isLogged = this.props.isLogged
            const redirect = this.state.redirect
            if (isLogged === true) return <Component {...this.props} />
            if (redirect === true) return <Redirect to={{pathname: "/login", state: { from: this.props.location}}} />
            return <LoginBouncer />

        }
    }
}


