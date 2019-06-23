import React from 'react'
import { connect } from 'react-redux'
import withImmutablePropsToJS from 'with-immutable-props-to-js'

import Login  from '../components/login'
import { logUser } from '../redux/actions/async'
import { isUserLogged, getLoggingStatus } from '../redux/selectors'

class LoginContainer extends React.Component {

    render() {
        return <Login isLogged={this.props.isLogged} logUser={this.props.logUser} loginStatus={this.props.loginStatus} from={this.props.from}/>
    }
}

const mapStateToProps = (state, ownProps) => ({
    isLogged: isUserLogged(state),
    loginStatus: getLoggingStatus(state),
    from: ownProps.location.state && ownProps.location.state.from
})

const mapDispatchToProps = { logUser }

export default connect(mapStateToProps, mapDispatchToProps)(withImmutablePropsToJS(LoginContainer))