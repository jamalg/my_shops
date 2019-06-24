import React from 'react'

import PlaceCard from '../place'
import './style.css'

export const Nearby = ({ places, addLike, addDisLike }) => (
    <div className="nearby-wrapper">
        <div className="places">
            {places.sort((p,p_) => p.distanceToLocation - p_.distanceToLocation).map(place => (
                <PlaceCard
                    key={place.id}
                    {...place}
                    addLike={addLike}
                    addDisLike={addDisLike}
                />
            )
            )}
        </div>
    </div>
)