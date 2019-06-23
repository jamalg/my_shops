import React from 'react'

import './style.css'

export const Requesting = () => (
    <div className="status-requesting-wrapper p-5">
        <p className="col lead text-center">
            Retreiving data from server !
        </p>
        <div className="text-center">
            <span className="col-1-sm text-primary spinner-grow mx-1"></span>
            <span className="col-1-sm text-secondary spinner-grow mx-1"></span>
            <span className="col-1-sm text-success spinner-grow mx-1"></span>
            <span className="col-1-sm text-danger spinner-grow mx-1"></span>
            <span className="col-1-sm text-warning spinner-grow mx-1"></span>
            <span className="col-1-sm text-info spinner-grow mx-1"></span>
            <span className="col-1-sm text-dark spinner-grow mx-1"></span>
        </div>
    </div>
)

export const Failed = () => (
    <div className="status-failed-wrapper p-5">
        <p className="col lead text-danger text-center">
            Oops... something seems wrong
        </p>
    </div>
)
