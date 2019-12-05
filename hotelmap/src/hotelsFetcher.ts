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

export function fetchByUrl(url: string, store: Function) {
    // TODO: solve CORS issue
    fetch(url.replace(':8080', ':3000')).then(
        response => response.json()
    ).then(
        data => store(data)
    )
}

export function fetchByLocation(lat: number, lon: number, 
                                store: Function, updateHistory: boolean = true) {
    let fullStore = store;                                    
    if (updateHistory) {
        fullStore = (data: hotelsData) => {
            window.history.pushState(
                {lat, lon},
                'Lime Home Test',
                `/?lat=${lat}&lon=${lon}`
            )
            store(data);
        }
    }
    return fetchByUrl(`/api/hotels/?lat=${lat}&lon=${lon}`, fullStore)
}