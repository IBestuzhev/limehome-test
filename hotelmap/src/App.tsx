import React, { useState, useEffect } from 'react';
import { fetchByLocation, fetchByUrl, hotelsData } from "./hotelsFetcher";
import './App.css';
import { HotelsList } from './hotelsList';
import { MapComponent } from "./mapComponent";


const App: React.FC = () => {
  const [hotels, storeHotels] = useState<hotelsData>({
    'previous': null,
    'next': null,
    'results': []
  });

  let urlQuery = new URLSearchParams(window.location.search);

  //52.5219, 13.38066
  const [searchPos, updateSearchPos] = useState<number[]>([
    parseFloat(urlQuery.get('lat') || '52.5219'),
    parseFloat(urlQuery.get('lon') || '13.38066')
  ]);
  const [nextSearchPos, updateNextSearchPos] = useState([...searchPos]);

  useEffect(() => {
    let shouldPushState = !(urlQuery.has('lat') && urlQuery.has('lon'));
    fetchByLocation(searchPos[0], searchPos[1], storeHotels, shouldPushState);
  }, [])

  useEffect(() => {
    window.onpopstate = (stateEvent: PopStateEvent) => {
      const state: {lat: number, lon: number} = stateEvent.state;
      if (state.lon && state.lat) {
        fetchByLocation(state.lat, state.lon, storeHotels, false);
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
          <h1 className="main-header__title">🌐 Hotel lookup</h1>
        </div>
      </header>
      <div className="wrapper main-wrapper">
        <div className="map-block">
          <MapComponent 
            hotels={hotels}
            searchPos={searchPos}
            nextSearchPos={nextSearchPos}
            updateNextSearchPos={updateNextSearchPos}
            searchClick={() => {
              fetchByLocation(nextSearchPos[0], nextSearchPos[1], (data: hotelsData) => {
                storeHotels(data);
                updateSearchPos([...nextSearchPos]);
              });
            }}
          />
        </div>
        <div className="list-block">
          <HotelsList hotels={hotels} paginator={(url => fetchByUrl(url, storeHotels))} />
        </div>
      </div>
      {/* {JSON.stringify(hotels)} */}
    </div>
  );
}

export default App;