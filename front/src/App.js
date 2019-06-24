import React from 'react';
import { Route } from 'react-router-dom'

import Header from './containers/header'
import Home from './containers/home'
import Login from './containers/login'
import Register from './components/register'
import Nearby from './containers/nearby'
import Liked from './containers/liked'
import './App.css';


export default function() {
  return (
    <div className="app-body w-100">
      <div className="app-wrapper container d-flex flex-column">
          <Route path="/" component={Header} />
          <Route exact path="/" component={Home} />
          <Route exact path="/login" component={Login} />
          <Route exact path="/register" component={Register} />
          <Route exact path="/nearby" component={Nearby} />
          <Route exact path="/liked" component={Liked} />
      </div>
    </div>
  )
}