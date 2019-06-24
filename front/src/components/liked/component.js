import React from 'react'

import PlaceCard from '../place'
import './style.css'

export const Liked = ({ places}) => (
    <div className="liked-wrapper">
        <div className="places">
            {places.map(place => (
                <PlaceCard
                    key={place.id}
                    {...place}
                />
            )
            )}
        </div>
    </div>
)