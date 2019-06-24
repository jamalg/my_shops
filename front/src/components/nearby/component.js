import React from 'react'

import './style.css'

const PlaceCard = ({name, photoUrl}) => (
    <div className="place-card">
        <div className="place-card-title">{name}</div>
        <img className="place-card-image" src={photoUrl} alt={`Illustration for ${name}`} />
    </div>
)

export const Nearby = ({ places }) => (
    <div className="nearby-wrapper">
        <div className="places">
            {places.sort((p,p_) => p.distanceToLocation - p_.distanceToLocation).map(place => <PlaceCard key={place.id} {...place} />)}
        </div>
    </div>
)