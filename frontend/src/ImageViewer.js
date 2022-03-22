import React from "react";
import "./ImageViewer.css";
import "./Game.css";
import { Typography } from "@mui/material";

function ImageViewer(props) {
    return props.image == null
        ? (
            <div id="imageViewer">
                <Typography className="textLabel" variant="h6" component="div" gutterBottom>
                    Loading image, please wait.
                </Typography>
            </div>
        )
        : (<div id="imageViewer">
            <Typography className="textLabel" variant="h6" component="div" gutterBottom>
                Guess the location of this image!
            </Typography>
            <div>
                <img id="geoImage" src={`data:image/jpeg;base64,${props.image}`} />
            </div>
        </div>)
}

export default ImageViewer;
