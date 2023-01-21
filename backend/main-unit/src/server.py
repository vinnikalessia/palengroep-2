from asyncio import Queue

import uvicorn
from uvicorn.config import LOGGING_CONFIG

from controllers.mqtt import MQTTController
from controllers.rest import RestController
from controllers.socketio import SocketIOController
from repositories.games import GameRepository

from services.game_service import GameService

LOGGING_CONFIG["formatters"]["default"]["fmt"] = "%(asctime)s [%(name)s] %(levelprefix)s %(message)s"

message_queue = Queue()

game_service = GameService(GameRepository(), message_queue)

rest_controller = RestController(game_service)
app = rest_controller.setup_endpoints()

socketio_controller = SocketIOController(app, game_service)
sio = socketio_controller.setup_endpoints()

mqtt_controller = MQTTController(game_service, message_queue)
mqtt = mqtt_controller.setup_endpoints()

game_service.set_socket_manager(socketio_controller.sio)
game_service.set_mqtt_client(mqtt)

mqtt.init_app(app)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3000)
