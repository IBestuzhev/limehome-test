export interface hotelsData {
    previous: string | null,
    next: string | null,
    results: any
}

export function fetchByUrl(url: string, store: Function) {
    // TODO: solve CORS issue
    fetch(url.replace(':8080', ':3000')).then(
        response => response.json()
    ).then(
        data => store(data)
    )
}

export function fetchByLocation(lat: number, lon: number, store: Function) {
    return fetchByUrl(`/api/hotels/?lat=${lat}&lon=${lon}`, store)
}