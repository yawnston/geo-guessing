import { Popover } from "@mui/material";
import { Icon } from "leaflet";
import { useState } from "react";
import { MapContainer, Marker, Popup, TileLayer, Tooltip, useMapEvents } from "react-leaflet";
import "./GameMap.css";
const React = require("react");


function PickedMarker(props) {
    const map = useMapEvents({
        click(clickEvent) {
            if (props.isPickingEnabled) {
                props.onPlayerPositionChange(clickEvent.latlng);
            }
        },
    });

    return props.playerPosition === null ? null : (
        <Marker position={props.playerPosition} >
            <Tooltip permanent={true}>Your guess</Tooltip>
        </Marker>
    )
}

function GameMap(props) {
    return (
        <MapContainer center={{ lat: 52.0, lng: 14.0 }} zoom={13} scrollWheelZoom={true}>
            <TileLayer
                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            />
            <PickedMarker isPickingEnabled={props.isPickingEnabled}
                playerPosition={props.playerPosition}
                onPlayerPositionChange={props.onPlayerPositionChange} />
        </MapContainer>
    )
}


export default GameMap;
