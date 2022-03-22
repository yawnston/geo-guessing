import React, { useEffect, useState } from "react";
import { Component } from "react";
import Button from "@mui/material/Button";
import GameMap from "./GameMap";
import "./Game.css";
import ImageViewer from "./ImageViewer";
import { Typography } from "@mui/material";
import { getProblemInstance } from "./ApiClient";


function Game() {
    useEffect(() => {
        getProblemInstance().then(res => {
            setProblem(res);
        })
    }, []);
    const [problem, setProblem] = useState(null);
    const [round, setRound] = useState(1);
    const [playerScoreTotal, setPlayerScoreTotal] = useState(0);
    const [aiScoreTotal, setAiScoreTotal] = useState(0);
    const [playerPosition, setPlayerPosition] = useState(null);
    const [aiPosition, setAiPosition] = useState(null);
    const [correctPosition, setCorrectPosition] = useState(null);
    const [isRoundOver, setIsRoundOver] = useState(false);
    const [isGameOver, setIsGameOver] = useState(false);
    const MAX_ROUNDS = 5;

    const handlePlayerPositionChange = (newPosition) => {
        setPlayerPosition(newPosition);
    };

    const onGuessButtonClick = () => {
        setIsRoundOver(true);
        setAiPosition({ lat: 0.0, lon: 0.0 });
        setCorrectPosition({ lat: 0.0, lon: 0.0 });
        setPlayerScoreTotal(playerScoreTotal + 1);
        setAiScoreTotal(aiScoreTotal + 2);
    };

    const onContinueButtonClick = () => {
        if (round === MAX_ROUNDS) {
            // TODO: show summary
            setIsGameOver(true);
        } else {
            setIsRoundOver(false);
            setRound(round + 1);
            setPlayerPosition(null);
            setAiPosition(null);
            setCorrectPosition(null);
        }
    }

    const isGuessButtonDisabled = (isRoundOver || playerPosition === null || isGameOver);
    const isContinueButtonDisabled = (!isRoundOver || isGameOver);

    return (<div id="gameContainer">
        <div id="gameHeader">
            <Typography className="textLabel" variant="h5" component="div" gutterBottom>
                Round {round} of {MAX_ROUNDS}. Your score total is {playerScoreTotal} and the AI's score total is {aiScoreTotal}.
            </Typography>
            <div id="controlButtonsContainer">
                <Button className="gameButton" size="large"
                    disabled={isGuessButtonDisabled} variant="contained"
                    onClick={onGuessButtonClick}>
                    Make guess!
                </Button>
                <Button className="gameButton" color="success" size="large" variant="contained"
                    disabled={isContinueButtonDisabled}
                    onClick={onContinueButtonClick}>
                    Continue
                </Button>
            </div>
        </div>
        <div id="gameArea">
            <div id="imageToGuess">
                <ImageViewer image={problem?.image_base64} />
            </div>
            <div id="gameMap">
                <GameMap isPickingEnabled={true}
                    playerPosition={playerPosition}
                    onPlayerPositionChange={handlePlayerPositionChange} />
            </div>
        </div>
    </div>)
}

export default Game;

