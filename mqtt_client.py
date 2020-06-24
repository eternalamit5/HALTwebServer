from flask_mqtt import Mqtt
from paho.mqtt.client import MQTT_ERR_SUCCESS
from flask import flash, redirect
from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, BooleanField, SubmitField, PasswordField, RadioField, TextAreaField
from wtforms.validators import DataRequired


class RingBuf:
    def __init__(self, size):
        self.size = size
        self.item_list = []

    def append(self, x):
        if len(self.item_list) >= self.size:
            del self.item_list[0]
            self.item_list.append(x)
        else:
            self.item_list.append(x)

    def clear(self):
        self.item_list.clear()

    def print(self):
        for item in self.item_list:
            print(item)


class MqttClient:
    def __init__(self):
        self.mqtt = Mqtt()
        self.mqttclient_pub_topic_list = []
        self.mqttclient_sub_topic_list = []
        self.recv_msg_buffer = RingBuf(15)
        self.is_mqtt_client_connected = False

    def add_publish_topic(self, topic):
        # check for duplicate topics
        for item in self.mqttclient_pub_topic_list:
            if topic in item:
                return False

        # add topic to the list
        new_item = (topic, topic)
        self.mqttclient_pub_topic_list.append(new_item)
        return True

    def add_subscription_topic(self, topic):
        # check for duplicate topics
        for item in self.mqttclient_sub_topic_list:
            if topic in item:
                return False

        # add topic to the list
        new_item = (topic, topic)
        self.mqttclient_sub_topic_list.append(new_item)
        # Subscribe this topic
        self.mqtt.subscribe(topic)
        return True

    def rm_publish_topic(self, topic):
        # check for duplicate topics
        for item in self.mqttclient_pub_topic_list:
            if topic in item:
                # add topic to the list
                self.mqttclient_pub_topic_list.remove(item)
                return True
        return False

    def rm_subscription_topic(self, topic):
        # check for duplicate topics
        for item in self.mqttclient_sub_topic_list:
            if topic in item:
                # add topic to the list
                self.mqttclient_sub_topic_list.remove(item)

                # unsubscribe this topic
                self.mqtt.unsubscribe(topic)
                return True
        return False

    def get_status(self):
        return self.is_mqtt_client_connected

    def on_message_send(self, topic, message, qos):
        if topic != "" and message != "":
            [result, b] = self.mqtt.publish(topic, message, int(qos))
            if result == MQTT_ERR_SUCCESS:
                return True
        return False

    def on_message_receive(self, topic, data):
        message = topic + " : " + data
        self.recv_msg_buffer.append(message)
        print("added")

    def update(self):
        if self.recv_msg_buffer.item_list:
            output = ""
            for item in self.recv_msg_buffer.item_list:
                output = output + item + "\n"
            return output
        return None


flask_mqtt_client = MqttClient()


@flask_mqtt_client.mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    flask_mqtt_client.is_mqtt_client_connected = True


@flask_mqtt_client.mqtt.on_disconnect()
def handle_disconnect(client, userdata, flags, rc):
    flask_mqtt_client.is_mqtt_client_connected = False


@flask_mqtt_client.mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    flask_mqtt_client.on_message_receive(message.topic, message.payload.decode())


class MqttClientAppForm(FlaskForm):
    is_client_connected = False

    pub_topic_add = StringField('Topic')
    pub_add = SubmitField('Add')

    sub_topic_add = StringField('Topic')
    sub_add = SubmitField('Add')
    sub_qos_add = SelectField('QoS', choices=[(0, '0'), (1, '1'), (2, '2')])

    pub_topic_rm = SelectField('Topic', choices=flask_mqtt_client.mqttclient_pub_topic_list)
    pub_rm = SubmitField('Remove')

    sub_topic_rm = SelectField('Topic', choices=flask_mqtt_client.mqttclient_sub_topic_list)
    sub_rm = SubmitField('Remove')

    pub_topic = SelectField('Topic', choices=flask_mqtt_client.mqttclient_pub_topic_list)
    pub_data = StringField('Message')
    pub_qos_add = SelectField('QoS', choices=[(0, '0'), (1, '1'), (2, '2')])

    send = SubmitField('Send')
