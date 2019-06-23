import React from 'react'
import { connect } from 'react-redux'
import withImmutablePropsToJS from 'with-immutable-props-to-js'

import Header  from '../components/header'
import { userLogout } from '../redux/actions/sync'
import { isUserLogged } from '../redux/selectors'

class HeaderContainer extends React.Component {

    render() {
        return <Header isLogged={this.props.isLogged} logoutUser={this.props.userLogout}/>
    }
}

const mapStateToProps = (state) => ({
    isLogged: isUserLogged(state),
})
const mapDispatchToProps = { userLogout }

export default connect(mapStateToProps, mapDispatchToProps)(withImmutablePropsToJS(HeaderContainer))