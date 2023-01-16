# basic hello world fastapi app

from fastapi_mqtt.fastmqtt import FastMQTT
from fastapi import FastAPI, Request
from fastapi_mqtt.config import MQTTConfig

import uvicorn
from pydantic import BaseModel
from starlette.responses import RedirectResponse

from models.setup_model import SetupModel

app = FastAPI()
mqtt_config = MQTTConfig()
mqtt_config.host = "mqtt"

mqtt = FastMQTT(config=mqtt_config)
mqtt.init_app(app)


@mqtt.on_connect()
def connect(client, flags, rc, properties):
    mqtt.client.subscribe("/mqtt")  # subscribing mqtt topic
    print("Connected: ", client, flags, rc, properties)


@mqtt.on_message()
async def message(client, topic, payload, qos, properties):
    print("Received message: ", topic, payload.decode(), qos, properties)
    return 0


@mqtt.subscribe("foobar")
async def message_to_topic(client, topic, payload, qos, properties):
    print("Received message to specific topic: ", topic, payload.decode(), qos, properties)


@app.get("/")
async def root():
    # returns a simple hello world message
    return RedirectResponse(url="/docs")


@app.get("/games")
async def get_games():
    return {
        "games": [
            {
                "name": "Red/Blue",
                "description": "bla bla bla bla bla",
                "players": "minimum 2",
                "num_teams": 2,
            },
            {
                "name": "Zen",
                "description": "bla bla bla bla bla",
                "players": "minimum 2",
                "num_teams": 1,
            },
            {
                "name": "Simon Says",
                "description": "bla bla bla bla bla",
                "players": "minimum 2",
                "num_teams": 1,
            },
        ]
    }


@app.get("/leaderboard/{game}/{difficulty}")
async def get_leaderboard(game: str, difficulty: str):
    return {
        "leaderboard": {
            "game": game,
            "difficulty": difficulty,
            "daily": [
                {
                    "teamName": "Team 1",
                    "score": 100,
                },
                {
                    "teamName": "Team 1",
                    "score": 99,
                },
                {
                    "teamName": "Team 1",
                    "score": 50,
                },
                {
                    "teamName": "Team 1",
                    "score": 25,
                }],
            "alltime": [
                {
                    "teamName": "Team 1",
                    "score": 100,
                },
                {
                    "teamName": "Team 1",
                    "score": 99,
                },
                {
                    "teamName": "Team 1",
                    "score": 50,
                },
                {
                    "teamName": "Team 1",
                    "score": 25,
                }],
        }
    }


@app.get("/score")
async def get_score():
    return {
        "game": "Red/Blue",
        "difficulty": "traag",
        "score": {
            "team1": 100,
            "team2": 50,
        },
    }


@app.post("/setup")
async def setup(setup_config: SetupModel):
    """
    post request which gets game name, 2 teamnames, a duration and a difficulty setting from the body
    :return:
    """
    game = setup_config.game
    difficulty = setup_config.difficulty
    team1_name = setup_config.teamNames[0]
    team2_name = setup_config.teamNames[1]
    duration = setup_config.duration

    return {
        "game": game,
        "teams": {
            "team1": team1_name,
            "team2": team2_name,
        },
        "duration": duration,
        "difficulty": difficulty,
        "status": "starting",
    }


# uvicorn server

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0",
                port=3000)
