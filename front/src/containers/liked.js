import React from 'react'
import { connect } from 'react-redux'
import withImmutablePropsToJS from 'with-immutable-props-to-js'

import Liked from '../components/liked'
import { fetchLiked, deleteLike } from '../redux/actions/async'
import { getLikedPlaces, getLikedFetchStatus, isUserLogged } from '../redux/selectors'


class LikedContainer extends React.Component {
    componentDidMount() {
        this.props.fetchLiked()
    }

    render() {
        return <Liked
                    places={this.props.places}
                    status={this.props.status}
                    isLogged={this.props.isLogged}
                    deleteLike={this.props.deleteLike}
                />
    }
}

const mapStateToProps = (state) => ({
    isLogged: isUserLogged(state),
    places: getLikedPlaces(state),
    status: getLikedFetchStatus(state),
})

const mapDispatchToProps = {
    fetchLiked,
    deleteLike
}

export default connect(mapStateToProps, mapDispatchToProps)(withImmutablePropsToJS(LikedContainer))
