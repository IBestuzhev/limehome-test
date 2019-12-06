import React from 'react';
import { hotelsData } from './hotelsFetcher';


type paginationProcessor = (url: string) => void;
type propType = {
    'hotels': hotelsData, 
    paginator: paginationProcessor, 
    activeHotel: number,
    setActiveHotel: (n: number) => void,
}

export const HotelsList: React.FC<propType> = ({hotels, paginator, activeHotel, setActiveHotel}) => {
    return (
        <React.Fragment>
            <div className="list-block__panel">
                <button disabled={!hotels.previous} onClick={() => paginator(hotels.previous as string)}>
                    Closer
                </button>
            </div>

            <ul>
                {hotels.results.map((el) => (
                    <li 
                        key={el.id} 
                        className={'hotelCard' + ((el.id === activeHotel) ? ' hotelCard--active' : '')}
                        onClick={() => setActiveHotel(el.id)}
                    >
                        <div className="hotelCard__title" title={el.title}>
                            {el.title}
                        </div>
                        <div className="hotelCard__distance">
                            {el.distance.toFixed(0)} m
                        </div>
                        <div className="hotelCard__coords">
                            {el.position[0]}
                            <br/>
                            {el.position[1]}
                        </div>
                    </li>
                ))}
            </ul>
            <div className="list-block__panel">
                <button disabled={!hotels.next} onClick={() => paginator(hotels.next as string)}>
                    Further
                </button>
            </div>
        </React.Fragment>
    )
}
