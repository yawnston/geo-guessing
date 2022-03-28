# I trained an AI to play GeoGuessr and it sort of works

## How to run it

Assume that all following backend commands are run
in the root folder, and the frontend commands are
run in the `frontend` folder.

### Prerequisites

Python 3.8 or higher w/ pip, npm 8.3 or higher

### Install requirements - backend

`pip install -r requirements.txt`

### Run it - backend

`python main.py` or running `Debug API` debug config in VS Code
will run the backend at `localhost:8081`.

### Training the network yourself

If you want to train the network for yourself because you are
curious or bored (or both), you first have to download a dataset
of images. You should have a folder structure like
`data/<square_id>/<number>.jpg` for training images, and
`valdata/<square_id>/<number.jpg>` for validation images.
The functions in `get_dataset.py` can help you do that.
However, be aware that you need a Google Cloud Platform
API key configured in the code settings for that.
See the comments in `settings.py` for more details.

Then configure the network parameters as you wish in `model.py`.
Mainly you want to change the number of epochs, but you can
try using a different optimizer etc. also.

When ready, run `python model.py` and the model will get trained,
and then its parameters will be saved to a file on the configured
path.

*Note*: training it on a CPU will probably be super slow, so you
may want to train it on a GPU using a GPU-enabled PyTorch install.

### Install requirements - frontend

`npm install`

### Run it - frontend

`npm start` will run the frontend at `localhost:3000`.

## What it does

The frontend app displays a game similar to GeoGuessr - you are
presented with an image taken from Google Street View, and you
have to guess where in the world it's located. Or rather, this
is the more restricted "No Moving, Panning or Zooming" version
of GeoGuessr, where all you have to go on is a still image.
Even skilled human players often have trouble getting good
guesses consistently. So I thought - let's train an AI to do it!

When you make your guess, the AI (a trained neural network)
also makes a guess, and your guesses are displayed on the map,
along with the correct location for that guess. A score is
calculated using the GeoGuessr score formula, and after 5 rounds
of guessing, the player with the most points wins!

After playing with the AI for a bit, it's actually surprisingly good.
Its accuracy isn't perfect, but this is a task where even human players
will generally score pretty low scores, just because of how little
information there is. I found that the AI can easily keep up with
me, and even beating me more often than not. And I'm not a slouch
when it comes to GeoGuessr either!

In the GeoGuessr beta, the average score on the world map
was about 11000 points. Of course guessing in the entire
world is harder, but those players also got to move around, zoom
and pan as they wished. The AI gets none of those advantages,
and it's able to consistently score around or above that!
I'd say that's pretty solid.

## How it works

First of all, it's hard to get a neural network to guess
latitude and longitude. Therefore I let the network do something
which neural networks are good at - classification.

I divided an area in continenal Europe into a square grid,
numbering the squares with an ID number. What the AI then does
is that is tries to guess which square the image belongs in.
Using the probabilities for each square, the final guess
is calculated by weighing the squares' geographical locations
based on how confident the network is in that square being right.
This grid can be visualized by opening
[grid.html](./grid.html) from the
root directory in your browser.

Training a network from scratch is very time-comsuming, and
requires a **LOT** of data, which is a problem because getting
images from Street View's API costs real money. Therefore I decided
to go with a pre-trained network for image classifications
(ResNet 18), which is then fine-tuned for our task using
a custom dataset. The deep learning framework used is PyTorch.

This dataset consists of approximately 200 images for each
document class (map square) for training data, as well as
25 validation images for each class, which were not
used during training, and have never been seen by the network.

The model used in the final app was trained on this data
for 25 epochs, and achieved about 20% accuracy on the validation
dataset. For reference, random choice would achieve about
5.5% accuracy. But we are not just after accuracy - we want
the model to make geographical predictions. Therefore
even if the model guesses the wrong square, if the square it
guessed is close to the right square, we are still improving our
guess.

The model's parameters were saved to a file after training,
and these parameters are loaded when the API is starting.

## Code organization

- `main.py`: API created with FastAPI, including all API methods
- `get_dataset.py`: loading and saving image
datasets from Google Maps Street View
- `grid.py`: creating and visualizing the square map grid
- `model.py`: everything related to the neural network
- `guessing.py`: AI guessing algorithm, distance and score
measurements
- `settings.py`: loading and storing app settings
- `frontend` folder: React frontend code (not too interesting)
