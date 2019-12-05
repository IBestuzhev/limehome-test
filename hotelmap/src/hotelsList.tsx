import React from 'react';
import { hotelsData } from './hotelsFetcher';


type paginationProcessor = (url: string) => void;

export const HotelsList: React.FC<{'hotels': hotelsData, paginator: paginationProcessor}> = ({hotels, paginator}) => {
    return (
        <React.Fragment>
            <button disabled={!hotels.previous} onClick={() => paginator(hotels.previous as string)}>Closer</button>

            <ul>
                {hotels.results.map((el: any) => (
                    <li key={el.id}>
                        <strong>{el.title}</strong>
                        <span>&nbsp;
                            {el.distance.toFixed(2)} meters away
                        </span>
                    </li>
                ))}
            </ul>

            <button disabled={!hotels.next} onClick={() => paginator(hotels.next as string)}>Further</button>
        </React.Fragment>
    )
}
