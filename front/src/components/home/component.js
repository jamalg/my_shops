import React from 'react'
import { Link, Redirect } from 'react-router-dom'

import './style.css'


export const Home = ({ isLogged }) => {
    if (isLogged === true) return <Redirect to="/nearby" />
    return (
        <div className="home-wrapper">
            <main className="d-flex flex-column">
                <div className="main-content ml-3 my-auto">
                    <h1 className="mb-4">Welcome !</h1>
                    <p className="lead">
                        Discover shops nearby !
                    </p>
                    <p className="lead mt-4">
                        <Link to="/register" className="btn-lg btn-success text-center">Try it now !</Link>
                    </p>
                </div>
            </main>
        </div>
    )
}