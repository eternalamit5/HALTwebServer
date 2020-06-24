from flask_app import app
import logging
import eventlet
import json
from flask import Flask, render_template
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
from flask_bootstrap import Bootstrap
from flask_mqtt import Mqtt
from flask import flash, redirect
from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, BooleanField, SubmitField, PasswordField, RadioField, TextAreaField
from wtforms.validators import DataRequired

eventlet.monkey_patch()
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['MQTT_BROKER_URL'] = 'localhost'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_CLIENT_ID'] = 'flask_mqtt'
app.config['MQTT_CLEAN_SESSION'] = True
app.config['MQTT_USERNAME'] = ''
app.config['MQTT_PASSWORD'] = ''
app.config['MQTT_KEEPALIVE'] = 5
app.config['MQTT_TLS_ENABLED'] = False
app.config['MQTT_LAST_WILL_TOPIC'] = 'home/lastwill'
app.config['MQTT_LAST_WILL_MESSAGE'] = 'bye'
app.config['MQTT_LAST_WILL_QOS'] = 2
mqtt = Mqtt(app)
socketio = SocketIO(app)
bootstrap = Bootstrap(app)



class MqttClient:
    def __init__(self):
        self.mqttclient_pub_topic_list = []
        self.mqttclient_sub_topic_list = []
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


flask_mqtt_client = MqttClient()


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



@socketio.on('publish')
def handle_publish(json_str):
    data = json.loads(json_str)
    mqtt.publish(data['topic'], data['message'], data['qos'])


@socketio.on('subscribe')
def handle_subscribe(json_str):
    data = json.loads(json_str)
    mqtt.subscribe(data['topic'], data['qos'])


@socketio.on('unsubscribe_all')
def handle_unsubscribe_all():
    mqtt.unsubscribe_all()


@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    data = dict(
        topic=message.topic,
        payload=message.payload.decode(),
        qos=message.qos,
    )
    socketio.emit('mqtt_message', data=data)


@mqtt.on_log()
def handle_logging(client, userdata, level, buf):
    # print(level, buf)
    pass
