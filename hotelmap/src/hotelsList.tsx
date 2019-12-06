import React from 'react';
import { hotelsData } from './hotelsFetcher';


type paginationProcessor = (url: string) => void;
type propType = {
    'hotels': hotelsData, 
    paginator: paginationProcessor, 
    activeHotel: number,
    setActiveHotel: (n: number) => void,
}

function formatCoord(deg: number, coordType: 'lat' | 'lon'): string {
    let side = '';
    if (deg > 0) {
        side = (coordType === 'lon') ? 'E' : 'N';
    } else {
        side = (coordType === 'lon') ? 'W' : 'S';
    }
    // Inspired by https://stackoverflow.com/a/5786627/978434
    deg = Math.abs(deg);
    let d = Math.floor (deg);
    let minfloat = (deg - d) * 60;
    let m = Math.floor(minfloat);
    let secfloat = (minfloat - m) * 60;
    let s = Math.round(secfloat);

    // After rounding, the seconds might become 60. These two
    // if-tests are not necessary if no rounding is done.
    if (s === 60) {
        m++;
        s=0;
    }
    if (m === 60) {
        d++;
        m=0;
    }

    return `${side} ${d}° ${m}′ ${s}″`

}

export const HotelsList: React.FC<propType> = ({hotels, paginator, activeHotel, setActiveHotel}) => {
    return (
        <React.Fragment>
            <div className="list-block__panel">
                <button disabled={!hotels.previous} onClick={() => paginator(hotels.previous as string)}>
                    &larr; Closer
                </button>
                &nbsp;&nbsp;&nbsp;
                <button disabled={!hotels.next} onClick={() => paginator(hotels.next as string)}>
                    Further &rarr;
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
                            <div>{el.title}</div>

                            <div className="hotelCard__distance">
                                {el.distance.toFixed(0)} m
                            </div>

                        </div>
                        <div className="hotelCard__coords">
                            {formatCoord(el.position[0], 'lat')}
                            <br/>
                            {formatCoord(el.position[1], 'lon')}
                        </div>
                    </li>
                ))}
            </ul>
        </React.Fragment>
    )
}
