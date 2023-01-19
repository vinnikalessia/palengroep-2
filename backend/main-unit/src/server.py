from asyncio import Queue

from fastapi_mqtt.fastmqtt import FastMQTT
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_mqtt.config import MQTTConfig
from fastapi_socketio import SocketManager
import uvicorn
from starlette.background import BackgroundTasks
from uvicorn.config import LOGGING_CONFIG

from misc.game_queue import MQTTQueueItem
from models.leaderboard_models import LeaderboardResponse
from models.game_models import GameStatusResponse, GameScore, GameConfigModel, GamesResponse
from repositories.games import GameRepository

from routers.general import router as global_router
from services.games import GameService

mqtt_config = MQTTConfig()
mqtt_config.host = "mqtt"
mqtt = FastMQTT(config=mqtt_config)

app = FastAPI()
LOGGING_CONFIG["formatters"]["default"]["fmt"] = "%(asctime)s [%(name)s] %(levelprefix)s %(message)s"
sio = SocketManager(app=app, cors_allowed_origins="*")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=global_router)

message_queue = Queue()

game_service = GameService(GameRepository(), sio, mqtt, message_queue)


# region mqtt
@mqtt.on_connect()
def connect(client, flags, rc, properties):
    print("Connected: ", client, flags, rc, properties)


@mqtt.subscribe('unit/#')
async def message(client, topic, payload, qos, properties):
    # logging.info("Received message to specific topic: ", topic, payload.decode(), qos, properties)
    # print("Received message to specific topic: ", topic, payload.decode(), qos, properties, flush=True)

    await message_queue.put(MQTTQueueItem(topic, payload.decode()))


# endregion

# @app.websocket("/ws")
# def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     while True:
#         data = await websocket.receive_text()
#         await websocket.send_text(f"Message text was: {data}")

# region socketio
@sio.on("connect")
def connect(sid, environ):
    print("connect ", sid)


@sio.on('disconnect')
def disconnect(sid):
    print('disconnect ', sid)


# endregion

@app.get("/leaderboard/{game}/{difficulty}")
def get_leaderboard(game: str, difficulty: str) -> LeaderboardResponse:
    return LeaderboardResponse(leaderboard=game_service.get_leaderboard(game, difficulty))


@app.get("/score")
def get_score() -> GameScore:
    return game_service.get_score()


@app.post("/setup")
def setup(setup_config: GameConfigModel, background_tasks: BackgroundTasks) -> GameStatusResponse:
    """
    post request which gets game name, 2 teamnames, a duration and a difficulty setting from the body
    :return:
    """

    current_game = game_service.setup_game(setup_config)
    return current_game


@app.get("/games", description="Get all games")
def get_games() -> GamesResponse:
    return GamesResponse(games=game_service.get_games())


mqtt.init_app(app)
# uvicorn server

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0",
                port=3000)
