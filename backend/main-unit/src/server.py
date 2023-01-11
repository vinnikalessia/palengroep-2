# basic hello world fastapi app
from fastapi_mqtt.fastmqtt import FastMQTT
from fastapi import FastAPI
from fastapi_mqtt.config import MQTTConfig

import uvicorn

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
    return {"message": "Hello World"}


@app.get("/mqtt")
async def mqtt_rest_handler():
    # publishes a message to the mqtt broker
    mqtt.client.publish("foobar", "Hello World")
    return {"message": "Hello World"}


# uvicorn server

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0",
                port=3000)
