import React from 'react'
import { connect } from 'react-redux'
import withImmutablePropsToJS from 'with-immutable-props-to-js'

import Home  from '../components/home'
import { isUserLogged } from '../redux/selectors'


class HomeContainer extends React.Component {
    render() {
        return <Home isLogged={this.props.isLogged}/>
    }
}

const mapStateToProps = (state) => ({
    isLogged: isUserLogged(state),
})

export default connect(mapStateToProps)(withImmutablePropsToJS(HomeContainer))