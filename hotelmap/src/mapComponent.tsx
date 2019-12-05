import React, { useState } from "react";
import HEREMap, { Marker } from "here-maps-react";
import { HEvent } from "here-maps-react/dist/utils/map-events";
import { hotelsData } from "./hotelsFetcher";


type propTypes = {
    searchClick: () => void,
    searchPos: number[],
    nextSearchPos: number[],
    updateNextSearchPos: (a: number[]) => void,
    hotels: hotelsData
}


class ErrorBoundary extends React.Component<{}, { hasError: boolean }> {
    constructor(props: {}) {
        super(props);
        this.state = { hasError: false };
    }

    static getDerivedStateFromError(error: any) {
        // Update state so the next render will show the fallback UI.
        return { hasError: true };
    }

    componentDidCatch(error: any, errorInfo: any) {
        // You can also log the error to an error reporting service
        console.log(error);
        console.log(errorInfo)
        setTimeout(() => this.setState({ hasError: false }), 100)
    }

    render() {
        if (this.state.hasError) {
            // You can render any custom fallback UI
            return <em>maps will re-render soon...</em>;
        }

        return this.props.children;
    }
}

export const MapComponent: React.FC<propTypes> = (
    { searchPos, nextSearchPos, updateNextSearchPos, hotels, searchClick }
) => {

    const [zoom, setZoom] = useState<number>(12);

    return (
        <React.Fragment>
            <div className="map-block__map">
                <ErrorBoundary>
                    <HEREMap
                        appId="Tbu3xBVyM9dUB0HlkAfi"
                        appCode="96rvfoL4yKT9u9d79F8jag"
                        interactive={true}
                        center={{ lat: nextSearchPos[0], lng: nextSearchPos[1] }}
                        zoom={zoom}
                        onDragEnd={function (this: H.Map, e: H.mapevents.Event) {
                            const newCenter = this.getCenter();
                            updateNextSearchPos([newCenter.lat, newCenter.lng]);
                            setZoom(this.getZoom());
                        } as HEvent}
                    >
                        {hotels.results.map((el: any) => (
                            <Marker
                                lat={el.position[0]}
                                lng={el.position[1]}
                                bitmap={el.icon}
                                key={`marker-${el.id}`}
                            />
                        ))}
                    </HEREMap>
                </ErrorBoundary>
            </div>
            <p className="map-block__search-panel">
                <button
                    className="map-block__search-button"
                    disabled={searchPos[0] === nextSearchPos[0] && searchPos[1] === nextSearchPos[1]}
                    onClick={searchClick}
                >
                    Search this area
        </button>
            </p>
        </React.Fragment>
    )
}