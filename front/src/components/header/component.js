import React from 'react'

import { Link, NavLink } from 'react-router-dom'

import './style.css'

const Brand = () => (
    <div className="main-brand"><span style={{fontWeight: 600}}>S</span>hops</div>
)

export const Header = ({ isLogged, logoutUser }) => (
    <header className="main-header">
        <div className="navbar navbar-expand-md navbar-light">
            <div className="navbar-brand">
                <Link to="/">
                    <Brand/>
                </Link>
            </div>
            <button
                type="button"
                className="navbar-toggler"
                data-toggle="collapse"
                data-target="#main-navbar-nav"
                aria-controls="main-navbar-nav" aria-expanded={false} aria-label="Toggle Navigation"
            >
                <span className="navbar-toggler-icon"></span>
            </button>
            <div id="main-navbar-nav" className="collapse navbar-collapse">
                <nav className="navbar-nav ml-auto text-center">
                    {   isLogged === true &&
                        <li className="nav-item">
                            <NavLink to="/nearby" className="nav-link">
                                <span className="main-navbav-nav-text">Nearby Shops</span>
                            </NavLink>
                        </li>
                    }
                    {   isLogged === true &&
                        <li className="nav-item">
                            <NavLink to="/liked" className="nav-link">
                                <span className="main-navbav-nav-text">My preferred Shops</span>
                            </NavLink>
                        </li>
                    }
                    {
                        isLogged === true &&
                        <form className="form-inline justify-content-center" onSubmit={logoutUser}>
                            <button className="mx-1 btn btn-outline-primary">Sign out</button>
                        </form>
                    }
                    { isLogged !== true &&
                        <form className="form-inline justify-content-center">
                            <Link to="/login" className="mx-1 btn btn-outline-primary">Sign in</Link>
                            <Link to="/register" className="mx-1 btn btn-outline-primary">Sign up</Link>
                        </form>
                    }
                </nav>
            </div>
        </div>
    </header>
)
