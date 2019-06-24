import React from 'react'

import './style.css'

export const PlaceCard = ({id, name, photoUrl, addLike, addDisLike, deleteLike, likeId}) => (
    <div className="place-card">
        <div className="place-card-title">{name}</div>
        <img className="place-card-image" src={photoUrl} alt={`Illustration for ${name}`} />
        <div className="place-social mt-2">
            {addDisLike && <button onClick={() => addDisLike(id)} className="btn btn-danger col-6 mr-1" >Dislike</button>}
            {addLike && <button onClick={() => addLike(id)} className="btn btn-success col-6 mrl-1" >Like</button>}
            {deleteLike && <button onClick={() => deleteLike(likeId, id)} className="btn btn-danger col-6" >Remove</button>}
        </div>
    </div>
)