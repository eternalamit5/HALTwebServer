from flask import Flask
from datetime import timedelta
from mongodb_client import mongo
from mqtt_client import flask_mqtt_client
import settings

app = Flask(__name__)
app.permanent_session_lifetime = timedelta(days=1)
app.secret_key = "karshUniBremen"

# Mongo db setup
app.config["MONGO_URI"] = settings.MONGODB_URI
mongo.init_app(app)
user_db = mongo.db.user_collection
device_db = mongo.db.device_collection

# MQTT client
app.config['MQTT_BROKER_URL'] = settings.MQTT_BROKER_URL
app.config['MQTT_BROKER_PORT'] = settings.MQTT_BROKER_PORT
app.config['MQTT_USERNAME'] = settings.MQTT_BROKER_USR_NAME
app.config['MQTT_PASSWORD'] = settings.MQTT_BROKER_PASSWORD
app.config['MQTT_KEEPALIVE'] = 5  # set the time interval for sending a ping to the broker to 5 seconds
app.config['MQTT_TLS_ENABLED'] = False  # set TLS to disabled for testing purposes
if settings.MQTT_CLIENT_ENABLE:
    flask_mqtt_client.mqtt.init_app(app)