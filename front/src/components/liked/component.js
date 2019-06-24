import React from 'react'

import PlaceCard from '../place'
import './style.css'

export const Liked = ({ places, deleteLike}) => (
    <div className="liked-wrapper">
        <div className="places">
            {places.map(place => (
                <PlaceCard
                    key={place.id}
                    {...place}
                    deleteLike={deleteLike}
                />
            )
            )}
        </div>
    </div>
)