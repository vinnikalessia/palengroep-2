import random
import tkinter as tk
import uuid
import argparse

from paho.mqtt.client import Client

padding = dict(padx=10, pady=10)

font_bold = dict(font="Helvetica 18 bold")
font_default = dict(font="Helvetica 18")
font_smaller = dict(font="Helvetica 14")
widget_options = dict(**padding)

parser = argparse.ArgumentParser()
parser.add_argument("--ip", type=str, default="10.42.0.1", help="IP address of the MQTT broker")
parser.add_argument("--dialog", action="store_true", help="Run in dialog mode", default=False)
parser.add_argument("--autopilot", action="store_true", help="Enable autopilot", default=False)

args = parser.parse_args()

mqtt_ip = args.ip


class Runner:
    def __init__(self):
        self.uuid = str(uuid.uuid4())[0:8]
        self.mqtt = Client()

        self.root = None
        self.label_unit_number = None
        self.label_configured = None
        self.label_led_status = None
        self.button = None
        self.log_widget = None
        self.cb_autopilot = None

        self.autopilot_var = None

        self.status_after_press = lambda x: x
        self.current_status = "off"

    def on_autopilot_change(self):

        if self.autopilot_var.get():
            self.add_to_log("Autopilot enabled")
        else:
            self.add_to_log("Autopilot disabled")

    def init_tk(self):
        self.root = tk.Tk()
        if args.dialog:
            self.root.attributes('-type', 'dialog')
        self.root.title("Label and Button Example")
        self.root.protocol("WM_DELETE_WINDOW", self.root.destroy)

        self.label_unit_number = tk.Label(self.root, text=f"Unit: {self.uuid}", **widget_options, **font_bold)
        self.label_unit_number.pack()

        self.label_configured = tk.Label(self.root, text="Not configured", **widget_options, **font_smaller)
        self.label_configured.pack()

        self.label_led_status = tk.Label(self.root, text=f"LED status: {self.current_status}", **widget_options,
                                         **font_default)
        self.label_led_status.pack()

        self.autopilot_var = tk.BooleanVar(value=args.autopilot)

        self.cb_autopilot = tk.Checkbutton(self.root, text="Autopilot", command=self.on_autopilot_change,
                                           variable=self.autopilot_var, onvalue=True, offvalue=False,

                                           **widget_options, **font_smaller)
        self.cb_autopilot.pack()

        self.button = tk.Button(self.root, text="Druk op de paal",
                                command=self.on_button_press, **widget_options,
                                **font_bold)
        self.button.pack()

        self.log_widget = tk.Text(self.root, **widget_options)
        self.log_widget.pack()

        self.add_to_log("Log widget initialized")
        self.add_to_log(f"my uuid is {self.uuid}")

    def add_to_log(self, message):
        if not message.endswith("\n"):
            message += "\n"
        self.log_widget.insert(tk.END, message)
        self.log_widget.see("end")

    def on_mqtt_message(self, client, userdata, message):
        topic = message.topic
        payload = message.payload.decode()
        self.add_to_log(f"Received message on topic {topic}: {payload}")

        if topic.startswith("configure/"):
            last_part = topic.split("/")[-1]
            self.label_configured["text"] = f"Configured to: {last_part} = {payload}"

            if last_part == "on_press":
                if payload == "led_off":
                    self.status_after_press = lambda x: "off"
                elif payload == "led_on":
                    self.status_after_press = lambda x: "on"
                elif payload == "led_continue":
                    self.status_after_press = lambda x: x

        elif topic.startswith("command/") and topic.endswith("/light"):
            self.label_led_status["text"] = "LED status: " + payload

            if payload == 'off':
                self.label_led_status['bg'] = '#d9d9d9'
            elif payload.startswith('on'):
                _, r, g, b = payload.split(' ')
                r, g, b = int(r), int(g), int(b)
                hexcode = f'#{r:02x}{g:02x}{b:02x}'
                self.label_led_status['bg'] = hexcode

                if self.autopilot_var.get():
                    random_interval = random.randint(1000, 5000)
                    self.add_to_log(f"Autopilot is enabled, sending button press in {random_interval // 1000:.2f} s")
                    self.root.after(random_interval, self.on_button_press)

        elif topic == "notification/general":
            self.add_to_log(f"Received notification: {payload}")

            if payload == "GAME_START_NOTIFICATION":
                self.mqtt.publish(f"unit/{self.uuid}/alive", self.uuid)

    def on_button_press(self):
        self.mqtt.publish(f"unit/{self.uuid}/action", "button pressed")
        self.add_to_log("Button pressed")

        self.current_status = self.status_after_press(self.current_status)
        if self.current_status == 'off':
            self.label_led_status['bg'] = '#d9d9d9'
        elif self.current_status.startswith('on'):
            _, r, g, b = self.current_status.split(' ')
            r, g, b = int(r), int(g), int(b)
            hexcode = f'#{r:02x}{g:02x}{b:02x}'
            self.label_led_status['bg'] = hexcode
        self.label_led_status["text"] = f"LED status: {self.current_status}"

    def on_mqtt_disconnect(self, client, userdata, rc):
        self.add_to_log("MQTT disconnected, reconnecting...")
        self.mqtt.reconnect()
        self.add_to_log("MQTT reconnected")

    def on_mqtt_connect(self, client, userdata, flags, rc):
        self.add_to_log("MQTT connected")

    def run(self):
        self.init_tk()
        self.mqtt.on_message = self.on_mqtt_message
        self.mqtt.on_disconnect = self.on_mqtt_disconnect
        self.mqtt.on_connect = self.on_mqtt_connect

        self.mqtt.connect(mqtt_ip)
        self.mqtt.subscribe("configure/#")
        self.mqtt.subscribe(f"command/{self.uuid}/light")
        self.mqtt.subscribe(f"command/all/light")
        self.mqtt.subscribe("notification/general")
        self.mqtt.loop_start()
        self.root.mainloop()


if __name__ == "__main__":
    Runner().run()
