from flask import flash, redirect
from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, BooleanField, SubmitField, PasswordField, RadioField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from application import app, user_db, device_db, flask_mqtt_client


class LoginForm(FlaskForm):
    email = StringField('e-mail address', validators=[DataRequired(message='Please enter password'), Email()])
    password = PasswordField('Password', validators=[DataRequired(message='Please enter password')])
    remember_me = BooleanField('Remember Me')
    sign_in = SubmitField('Login')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(message='Please enter user name'), Length(min=2, max=20)])
    email = StringField('e-mail address', validators=[DataRequired(message='Please enter password'), Email()])
    password = PasswordField('Password', validators=[DataRequired(message='Please enter password')])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(message='Please re-enter password'), EqualTo(password)])

    register = SubmitField('Sign Up')


class DeviceStatusForm(FlaskForm):
    pass


class DeviceConfigurationForm(FlaskForm):
    config_modules = ['System', 'Sensor', 'Protocol', 'Storage']
    deviceID = StringField('Device ID', validators=[DataRequired(message='Please enter device ID')])
    configuration = RadioField('Select configuration module',
                               choices=config_modules, default='System')
    next = SubmitField('Next')
    new_device = BooleanField('Add as new device')


class SystemForm(FlaskForm):
    baud_rate_list = [('4800', '4800'), ('9600', '9600'), ('19200', '19200'), ('38400', '38400'),
                      ('57600', '57600'),
                      ('115200', '115200')]
    i2c_freq_list = [('50000', '50k'), ('100000', '100k'), ('200000', '200k'), ('400000', '400k')]
    dev_type = [('Gateway', 'Gateway'), ('Sensor Node', 'Sensor Node')]
    reconn_list = [('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'),
                   ('9', '9'), ('10', '10'), ('-1', 'Forever')]

    error_report_action = [('TURN_LED_OFF', 'TURN_LED_OFF'),
                           ('TURN_LED_ON', 'TURN_LED_ON'),
                           ('TOGGLE_LED_1HZ', 'TOGGLE_LED_1HZ'),
                           ('TOGGLE_LED_2HZ', 'TOGGLE_LED_2HZ'),
                           ('TOGGLE_LED_4HZ', 'TOGGLE_LED_4HZ'),
                           ('TERMINATE', 'TERMINATE'),
                           ('SPIN_FOREVER', 'SPIN_FOREVER'),
                           ('SOFTWARE_RESET', 'SOFTWARE_RESET'),
                           ('SEND_ERROR_MSG_MQTT', 'SEND_ERROR_MSG_MQTT'),
                           ('SEND_ERROR_MSG_BLE', 'SEND_ERROR_MSG_BLE'),
                           ('SEND_ERROR_MSG_SD_CARD_LOGGER', 'SEND_ERROR_MSG_SD_CARD_LOGGER'),
                           ('JUST_SHOW_DEBUG_LOG', 'JUST_SHOW_DEBUG_LOG')]

    device_type = SelectField('Device Type', choices=dev_type, default='Gateway')
    device_uuid = StringField('Device UUID', render_kw={'readonly': True})
    network_id = StringField('Network ID', validators=[DataRequired(message='Mandatory')])
    description = StringField('Description', validators=[DataRequired(message='Mandatory')])
    uart0_en = BooleanField('UART0 Enable', render_kw={'checked': False})
    uart0_baud = SelectField('UART0 Baud', choices=baud_rate_list, default='115200')
    uart1_en = BooleanField('UART1 Enable', render_kw={'checked': False})
    uart1_baud = SelectField('UART1 Baud', choices=baud_rate_list, default='115200')
    uart2_en = BooleanField('UART2 Enable', render_kw={'checked': False})
    uart2_baud = SelectField('UART2 Baud', choices=baud_rate_list, default='115200')
    i2c0_en = BooleanField('I2C0 Enable', render_kw={'checked': False})
    i2c0_freq = SelectField('I2C0 Frequency', choices=i2c_freq_list, default='400000')
    i2c1_en = BooleanField('I2C1 Enable', render_kw={'checked': False})
    i2c1_freq = SelectField('I2C1 Frequency', choices=i2c_freq_list, default='400000')
    i2c2_en = BooleanField('I2C2 Enable', render_kw={'checked': False})
    i2c2_freq = SelectField('I2C2 Frequency', choices=i2c_freq_list, default='400000')
    hsspi_en = BooleanField('High speed SPI Enable', render_kw={'checked': False})
    lsspi_en = BooleanField('Low speed SPI Enable', render_kw={'checked': False})
    wifi_en = BooleanField('Wifi Enable', render_kw={'checked': True})
    smart_conn_en = BooleanField('Wifi Smart Connect Enable', render_kw={'checked': False})
    wifi_reconn = SelectField('Wifi Reconnection Attempt', choices=reconn_list, default='1')
    ssid1 = StringField('SSID router 1', validators=[DataRequired(message='Mandatory')])
    password1 = StringField('Password router 1', validators=[DataRequired(message='Mandatory')])
    ssid2 = StringField('SSID router 2')
    password2 = StringField('Password router 2')
    ssid3 = StringField('SSID router 3')
    password3 = StringField('Password router 3')
    ssid4 = StringField('SSID router 4')
    password4 = StringField('Password router 4')
    ssid5 = StringField('SSID router 5')
    password5 = StringField('Password router 5')
    ssid6 = StringField('SSID router 6')
    password6 = StringField('Password router 6')
    ssid7 = StringField('SSID router 7')
    password7 = StringField('Password router 7')
    ssid8 = StringField('SSID router 8')
    password8 = StringField('Password router 8')
    ssid9 = StringField('SSID router 9')
    password9 = StringField('Password router 9')
    ssid10 = StringField('SSID router 10')
    password10 = StringField('Password router 10')
    status_indicator_en = BooleanField('Status Indicator Enable', render_kw={'checked': False})
    std_exception_action = SelectField('Action on standard exception', choices=error_report_action,
                                       default='TURN_LED_OFF')
    error_major_action = SelectField('Action on major error', choices=error_report_action,
                                     default='TURN_LED_OFF')
    error_minor_action = SelectField('Action on minor error', choices=error_report_action,
                                     default='TURN_LED_OFF')
    warn_major_action = SelectField('Action on major warning', choices=error_report_action,
                                    default='TOGGLE_LED_2HZ')
    warn_minor_action = SelectField('Action on minor warning', choices=error_report_action,
                                    default='TOGGLE_LED_4HZ')
    save = SubmitField('Save')
    upload = SubmitField('Upload to device')


class ProtocolForm(FlaskForm):
    device_uuid = StringField('Device UUID', render_kw={'readonly': True})
    mqtt_client_enable = BooleanField('Enable MQTT Client')
    mqtt_broker_uri = StringField('MQTT Client URI')
    mqtt_broker_port = StringField('MQTT Broker Port')
    keep_alive_timeout = StringField('Keep Alive Timeout')
    # Anivnaash add more parameters here

    save = SubmitField('Save')
    upload = SubmitField('Upload to device')


class StorageForm(FlaskForm):
    device_uuid = StringField('Device UUID', render_kw={'readonly': True})
    # Anivnaash add more parameters here

    save = SubmitField('Save')
    upload = SubmitField('Upload to device')


class SensorForm(FlaskForm):
    device_uuid = StringField('Device UUID', render_kw={'readonly': True})
    # Anivnaash add more parameters here

    save = SubmitField('Save')
    upload = SubmitField('Upload to device')


class MqttClientAppForm(FlaskForm):
    log_info = TextAreaField('Received messages', render_kw={"rows": 6, "cols": 80})
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

