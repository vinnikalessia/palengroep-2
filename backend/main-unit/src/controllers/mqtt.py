from fastapi_mqtt import MQTTConfig, FastMQTT

from misc.queue.mqtt import MQTTQueueItem


def extract_esp_id_from_topic(topic: str):
    return topic.split("/")[-1]


class MQTTController:
    def __init__(self, game_service, message_queue):
        self.mqtt_config = MQTTConfig()
        self.mqtt_config.host = "mqtt"
        self.mqtt = FastMQTT(config=self.mqtt_config)
        self.game_service = game_service
        self.message_queue = message_queue

    def init_app(self, app):
        self.mqtt.init_app(app)

    def setup_endpoints(self):
        @self.mqtt.on_connect()
        def connect(client, flags, rc, properties):
            print("Connected: ", client, flags, rc, properties)

        @self.mqtt.subscribe('unit/+/alive')
        async def alive(client, topic, payload, qos, properties):
            esp32_id = extract_esp_id_from_topic(topic)
            self.game_service.handle_esp32_alive(esp32_id)

        @self.mqtt.subscribe('unit/+/action')
        async def action(client, topic, payload, qos, properties):
            esp32_id = extract_esp_id_from_topic(topic)
            print(f"esp32 {esp32_id} action: {payload.decode()}")
            self.game_service.handle_pole_action(esp32_id, payload.decode())

        @self.mqtt.subscribe('unit/#')
        async def message(client, topic, payload, qos, properties):
            await self.message_queue.put(MQTTQueueItem(topic, payload.decode()))

        return self.mqtt
