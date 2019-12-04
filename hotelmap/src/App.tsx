import React, { useState } from 'react';
import { fetchByLocation, fetchByUrl, hotelsData } from "./hotelsFetcher";
import './App.css';
import { HotelsList } from './hotelsList';

const App: React.FC = () => {
  const [hotels, storeHotels] = useState<hotelsData & {empty?: boolean}>({
    'previous': null,
    'next': null,
    'results': [],
    'empty': true,
  })

  if (hotels.empty) {
    fetchByLocation(52.5219, 13.38066, storeHotels);
  }

  // TODO: Add map here
  // TODO: Style the app
  // TODO: Call fetchByLocation from some map point

  return (
    <div className="App">
      <HotelsList hotels={hotels} paginator={(url => fetchByUrl(url, storeHotels))} />
      {JSON.stringify(hotels)}
    </div>
  );
}

export default App;
