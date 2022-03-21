import base64
from io import BytesIO
from typing import List, Tuple
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from guessing import distance, predict_location, score

from model import GeoModel
from settings import SETTINGS

app = FastAPI()
model = GeoModel()
model.load_from_disk()


class GetProblemResponse(BaseModel):
    image_base64: str
    correct_location: Tuple[float, float]
    model_predicted_probabilities: List[float]
    model_predicted_location: Tuple[float, float]
    model_predicted_distance_km: float
    model_predicted_score: int


@app.get("/problem", response_model=GetProblemResponse)
def get_problem() -> GetProblemResponse:
    """Get a new instance of the geo guessing problem,
    returning the image to guess, as well as the location
    and score which the AI guessed, the correct location,
    and the distance guessed by the AI.
    """
    # TODO: save correct location when downloading from Google Street View?
    # Currently the "correct location" is just the center of the square where
    # the image is taken from.
    image, probabilities, correct_location = model.predict_random_image()

    image_bytes = BytesIO()
    image.save(image_bytes, format="JPEG")
    image_base64 = base64.b64encode(image_bytes.getvalue())

    # DEBUG
    image.save("out.jpeg")

    predicted_location = predict_location(probabilities)
    predicted_distance = distance(predicted_location, correct_location)
    predicted_score = score(predicted_distance)

    return GetProblemResponse(
        image_base64=image_base64,
        correct_location=correct_location,
        model_predicted_probabilities=probabilities,
        model_predicted_location=predicted_location,
        model_predicted_distance_km=predicted_distance,
        model_predicted_score=predicted_score,
    )


class PostGuessParams(BaseModel):
    correct_location: Tuple[float, float]
    guessed_location: Tuple[float, float]


class PostGuessResponse(BaseModel):
    distance_km: float
    score: int


@app.post("/guess", response_model=PostGuessResponse)
def post_guess(params: PostGuessParams) -> PostGuessResponse:
    """Make a guess using the guessed location provided
    in the request body. Also provided by the frontend
    is the correct location which was expected.

    Returns the distance between the guesses, as well
    as the score achieved by the player's guess.
    """
    guessed_distance_km = distance(params.guessed_location, params.correct_location)
    guessed_score = score(guessed_distance_km)

    return PostGuessResponse(
        distance_km=guessed_distance_km,
        score=guessed_score,
    )


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=SETTINGS.api_bind_host,
        port=SETTINGS.api_bind_port,
        reload=False,
    )
