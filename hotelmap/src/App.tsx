import React, { useState, useEffect } from 'react';
import { fetchByLocation, fetchByUrl, hotelsData } from "./hotelsFetcher";
import './App.css';
import { HotelsList } from './hotelsList';
import { MapComponent } from "./mapComponent";


//52.5219, 13.38066 - default to Berlin
const initLat = 52.5219;
const initLon = 13.38066;


const App: React.FC = () => {
  const [hotels, storeHotels] = useState<hotelsData>({
    'previous': null,
    'next': null,
    'results': []
  });


  const [searchPos, updateSearchPos] = useState<number[]>([ NaN, NaN ]);
  const [nextSearchPos, updateNextSearchPos] = useState([initLat, initLon]);
  const [activeHotel, setActiveHotel] = useState<number>(0);

  useEffect(() => {
    if (Number.isNaN(searchPos[0]) || Number.isNaN(searchPos[1])) {
      // Position not yet known
      return;
    }
    fetchByLocation(searchPos[0], searchPos[1], storeHotels);
  }, [searchPos])

  useEffect(() => {
    let urlQuery = new URLSearchParams(window.location.search);
    if (urlQuery.has('lat') || urlQuery.has('lon')) {
      // location was passed via URL, use it
      let queryLat = parseFloat(urlQuery.get('lat') || '52.5219');
      let queryLon = parseFloat(urlQuery.get('lon') || '13.38066')
      updateSearchPos([queryLat, queryLon]);
      updateNextSearchPos([queryLat, queryLon]);
      return;
    }

    if ("geolocation" in navigator) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          // get coords from browser
          updateSearchPos([position.coords.latitude, position.coords.longitude]);
          updateNextSearchPos([position.coords.latitude, position.coords.longitude]);
        },
        () => {
          // failed to get coords
          updateSearchPos([initLat, initLon]);
        }
      )
    } else {
      // No URL and location not available
      updateSearchPos([initLat, initLon]);
    }
  }, []); // Call this hook only when App is mounted

  useEffect(() => {
    window.onpopstate = (stateEvent: PopStateEvent) => {
      const state: {lat: number, lon: number} = stateEvent.state;
      if (state.lon && state.lat) {
        updateSearchPos([state.lat, state.lon]);
        updateNextSearchPos([state.lat, state.lon])
      }
    }

    return () => { window.onpopstate = null; }
  }, [])

  // TODO: Style the app

  return (
    <div className="App">
      <header className='main-header'>
        <div className="wrapper">
          <h1 className="main-header__title">
            <span role="img" aria-label="Globe">🌐 </span>
            Hotel lookup
          </h1>
        </div>
      </header>
      <div className="wrapper main-wrapper">
        <div className="map-block">
          <MapComponent 
            hotels={hotels.results}
            activeHotel={activeHotel}
            setActiveHotel={setActiveHotel}
            searchPos={searchPos}
            nextSearchPos={nextSearchPos}
            updateNextSearchPos={updateNextSearchPos}
            searchClick={() => {
              updateSearchPos([...nextSearchPos]);
            }}
          />
        </div>
        <div className="list-block">
          <HotelsList 
            hotels={hotels} 
            paginator={(url => fetchByUrl(url, storeHotels))} 
            activeHotel={activeHotel}
            setActiveHotel={setActiveHotel}
          />
        </div>
      </div>
      {/* {JSON.stringify(hotels)} */}
    </div>
  );
}

export default App;