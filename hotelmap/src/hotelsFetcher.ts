export interface hotelInfo {
    id: number,
    icon: string,
    title: string,
    distance: number,
    position: number[],
}

export interface hotelsData {
    previous: string | null,
    next: string | null,
    results: hotelInfo[],
}

export function fetchByUrl(url: string, store: (v: hotelsData) => void) {
    // TODO: solve CORS issue
    fetch(url.replace('http://localhost:8080', '')).then(
        response => response.json()
    ).then(
        data => store(data)
    )
}

export function fetchByLocation(lat: number, lon: number, 
                                store: (value: hotelsData) => void) {
    let fullStore = store;         
                               
    if (window.location.search !== `?lat=${lat}&lon=${lon}`) {
        fullStore = (value: hotelsData) => {
            window.history.pushState(
                {lat, lon},
                'Lime Home Test',
                `/?lat=${lat}&lon=${lon}`
            )
            store(value);
        }
    }
    return fetchByUrl(`/api/hotels/?lat=${lat}&lon=${lon}`, fullStore)
}