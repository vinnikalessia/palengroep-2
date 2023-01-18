from fastapi_mqtt.fastmqtt import FastMQTT
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_mqtt.config import MQTTConfig
from fastapi_socketio import SocketManager
import uvicorn
from starlette.websockets import WebSocket
from uvicorn.config import LOGGING_CONFIG

from models.leaderboard import LeaderboardResponse
from models.score import GameScore
from models.game_status import GameStatusResponse
from models.setup_game import SetupGamePayload
from repositories.games import GameRepository

from routers.general import router as global_router
from services.games import GameService

mqtt_config = MQTTConfig()
mqtt_config.host = "mqtt"
mqtt = FastMQTT(config=mqtt_config)

app = FastAPI()
LOGGING_CONFIG["formatters"]["default"]["fmt"] = "%(asctime)s [%(name)s] %(levelprefix)s %(message)s"
sio = SocketManager(app=app, cors_allowed_origins="*")
mqtt.init_app(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=global_router)

game_service = GameService(GameRepository())


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


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")


@sio.on("connect")
async def connect(sid, environ):
    print("connect ", sid)
    return


@sio.on('disconnect')
async def disconnect(sid):
    print('disconnect ', sid)
    return


@app.get("/leaderboard/{game}/{difficulty}")
async def get_leaderboard(game: str, difficulty: str) -> LeaderboardResponse:
    return LeaderboardResponse(leaderboard=game_service.get_leaderboard(game, difficulty))


@app.get("/score")
async def get_score() -> GameScore:
    return game_service.get_score()


@app.post("/setup")
async def setup(setup_config: SetupGamePayload) -> GameStatusResponse:
    """
    post request which gets game name, 2 teamnames, a duration and a difficulty setting from the body
    :return:
    """

    return game_service.start_game(setup_config)


# uvicorn server

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0",
                port=3000)
