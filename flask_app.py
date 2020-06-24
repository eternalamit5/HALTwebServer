from flask import Flask
from mqtt_client import flask_mqtt_client
from datetime import timedelta
from flask_pymongo import PyMongo
import settings
from flask_mail import Mail, Message
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.permanent_session_lifetime = timedelta(days=1)
app.secret_key = "karshUniBremen"

# Mongo db setup
mongo = PyMongo()
app.config["MONGO_URI"] = settings.MONGODB_URI
mongo.init_app(app)
user_db = mongo.db.user_collection
device_db = mongo.db.device_collection
bootstrap = Bootstrap(app)



# MQTT client
app.config['MQTT_BROKER_URL'] = settings.MQTT_BROKER_URL
app.config['MQTT_BROKER_PORT'] = settings.MQTT_BROKER_PORT
app.config['MQTT_USERNAME'] = settings.MQTT_BROKER_USR_NAME
app.config['MQTT_PASSWORD'] = settings.MQTT_BROKER_PASSWORD
app.config['MQTT_KEEPALIVE'] = 5  # set the time interval for sending a ping to the broker to 5 seconds
app.config['MQTT_TLS_ENABLED'] = False  # set TLS to disabled for testing purposes
if settings.MQTT_CLIENT_ENABLE:
    flask_mqtt_client.mqtt.init_app(app)




app.config['MAIL_SERVER'] = settings.MAIL_SERVER
app.config['MAIL_PORT'] = settings.MAIL_PORT
usr_rec = user_db.find_one({'username': 'admin'})
if usr_rec is not None:
    app.config['MAIL_USERNAME'] = usr_rec['e-mail']
    app.config['MAIL_PASSWORD'] = usr_rec['password']
else:
    app.config['MAIL_USERNAME'] = ''
    app.config['MAIL_PASSWORD'] = ''
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
if settings.EMAIL_ENABLE:
    mail = Mail(app)


