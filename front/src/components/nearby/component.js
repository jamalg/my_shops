import React from 'react'

import './style.css'

const PlaceCard = ({id, name, photoUrl, addLike, addDisLike}) => (
    <div className="place-card">
        <div className="place-card-title">{name}</div>
        <img className="place-card-image" src={photoUrl} alt={`Illustration for ${name}`} />
        <div className="place-social mt-2">
            <button onClick={() => addDisLike(id)} className="btn btn-danger col-6 mr-1" >Dislike</button>
            <button onClick={() => addLike(id)} className="btn btn-success col-6 mrl-1" >Like</button>
        </div>
    </div>
)

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