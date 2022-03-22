import React, { useEffect, useState } from "react";
import { Component } from "react";
import Button from "@mui/material/Button";
import GameMap from "./GameMap";
import "./Game.css";
import ImageViewer from "./ImageViewer";
import { Typography } from "@mui/material";
import { getProblemInstance, postGuess } from "./ApiClient";
import GameOverDialog from "./GameOverDialog";


function Game() {
    useEffect(() => {
        // Effectively equivalent to `componentDidMount()`, meaning
        // we are using this to load the initial problem on page load.
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

    const handleNewGame = () => {
        setProblem(null);
        setRound(1);
        setPlayerScoreTotal(0);
        setAiScoreTotal(0);
        setPlayerPosition(null);
        setAiPosition(null);
        setCorrectPosition(null);
        setIsRoundOver(false);
        setIsGameOver(false);

        getProblemInstance().then(res => {
            setProblem(res);
        })
    };

    const onGuessButtonClick = () => {
        setIsRoundOver(true);
        postGuess(problem.correct_location, [playerPosition.lat, playerPosition.lng])
            .then(res => {
                setAiPosition({
                    lat: problem.model_predicted_location[0],
                    lon: problem.model_predicted_location[1],
                });
                setCorrectPosition({
                    lat: problem.correct_location[0],
                    lon: problem.correct_location[1],
                });
                setPlayerScoreTotal(playerScoreTotal + res.score);
                setAiScoreTotal(aiScoreTotal + problem.model_predicted_score);
            });
    };

    const onContinueButtonClick = () => {
        if (round === MAX_ROUNDS) {
            setIsGameOver(true);
        } else {
            getProblemInstance().then(res => {
                setProblem(res);
                setIsRoundOver(false);
                setRound(round + 1);
                setPlayerPosition(null);
                setAiPosition(null);
                setCorrectPosition(null);
            });
        }
    }

    const isGuessButtonDisabled = (isRoundOver || playerPosition === null || isGameOver);
    const isContinueButtonDisabled = (!isRoundOver || isGameOver);

    return (
        <div>
            <div id="gameContainer">
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
                        <GameMap isPickingEnabled={!isRoundOver && !isGameOver}
                            playerPosition={playerPosition}
                            onPlayerPositionChange={handlePlayerPositionChange}
                            correctPosition={correctPosition}
                            aiPosition={aiPosition} />
                    </div>
                </div>
            </div>
            <GameOverDialog isGameOver={isGameOver} onNewGame={handleNewGame}
                playerScoreTotal={playerScoreTotal} aiScoreTotal={aiScoreTotal} />
        </div>
    )
}

export default Game;

