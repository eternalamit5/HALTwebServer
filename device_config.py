from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, BooleanField, SubmitField, RadioField
from wtforms.validators import DataRequired
from flask_app import device_db


# ==================== Device configuration page ==============================
class DeviceConfigurationForm(FlaskForm):
    config_modules = ['System', 'Sensor', 'Protocol', 'Storage']
    deviceID = StringField('Device ID', validators=[DataRequired(message='Please enter device ID')])
    configuration = RadioField('Select configuration module',
                               choices=config_modules, default='System')
    next = SubmitField('Next')
    new_device = BooleanField('Add as new device')


# ==================== System configuration page ==============================
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


class SystemFormAttributes:
    @staticmethod
    def update_db(form):
        if form.device_uuid.data is not None:
            dev_rec = device_db.find_one({'device_uuid': form.device_uuid.data, 'doc_type': 'system'})
            if dev_rec is not None:
                # document with matching device id found
                dev_rec['device_type'] = form.device_type.data
                dev_rec['device_uuid'] = form.device_uuid.data
                dev_rec['network_id'] = form.network_id.data
                dev_rec['description'] = form.description.data
                dev_rec['uart0_en'] = form.uart0_en.data
                dev_rec['uart0_baud'] = form.uart0_baud.data
                dev_rec['uart1_en'] = form.uart1_en.data
                dev_rec['uart1_baud'] = form.uart1_baud.data
                dev_rec['uart2_en'] = form.uart2_en.data
                dev_rec["uart2_baud"] = form.uart2_baud.data
                dev_rec["i2c0_en"] = form.i2c0_en.data
                dev_rec["i2c0_freq"] = form.i2c0_freq.data
                dev_rec["i2c1_en"] = form.i2c1_en.data
                dev_rec["i2c1_freq"] = form.i2c1_freq.data
                dev_rec["hsspi_en"] = form.hsspi_en.data
                dev_rec["lsspi_en"] = form.lsspi_en.data
                dev_rec["wifi_en"] = form.wifi_en.data
                dev_rec["wifi_smartconnect_en"] = form.smart_conn_en.data
                dev_rec["wifi_reconnect_attempt"] = form.wifi_reconn.data
                dev_rec["ssid1"] = form.ssid1.data
                dev_rec["password1"] = form.password1.data
                dev_rec["ssid2"] = form.ssid2.data
                dev_rec["password2"] = form.password2.data
                dev_rec["ssid3"] = form.ssid3.data
                dev_rec["password3"] = form.password3.data
                dev_rec["ssid4"] = form.ssid4.data
                dev_rec["password4"] = form.password4.data
                dev_rec["ssid5"] = form.ssid5.data
                dev_rec["password5"] = form.password5.data
                dev_rec["ssid6"] = form.ssid6.data
                dev_rec["password6"] = form.password6.data
                dev_rec["ssid7"] = form.ssid7.data
                dev_rec["password7"] = form.password7.data
                dev_rec["ssid8"] = form.ssid8.data
                dev_rec["password8"] = form.password8.data
                dev_rec["ssid9"] = form.ssid9.data
                dev_rec["password9"] = form.password9.data
                dev_rec["ssid10"] = form.ssid10.data
                dev_rec["password10"] = form.password10.data
                dev_rec["indicator_en"] = form.status_indicator_en.data
                dev_rec["std_exception"] = form.std_exception_action.data
                dev_rec["error_major"] = form.error_major_action.data
                dev_rec["error_minor"] = form.error_minor_action.data
                dev_rec["warn_major"] = form.warn_major_action.data
                dev_rec["warn_minor"] = form.warn_minor_action.data

                device_db.save(dev_rec)
            else:
                # document with matching device id does not exists, so create new document in db
                device_db.insert({
                    'doc_type': 'system',
                    'device_type': form.device_type.data,
                    'device_uuid': form.device_uuid.data,
                    'network_id': form.network_id.data,
                    'description': form.description.data,
                    'uart0_en': form.uart0_en.data,
                    'uart0_baud': form.uart0_baud.data,
                    'uart1_en': form.uart1_en.data,
                    'uart1_baud': form.uart1_baud.data,
                    'uart2_en': form.uart2_en.data,
                    "uart2_baud": form.uart2_baud.data,
                    "i2c0_en": form.i2c0_en.data,
                    "i2c0_freq": form.i2c0_freq.data,
                    "i2c1_en": form.i2c1_en.data,
                    "i2c1_freq": form.i2c1_freq.data,
                    "hsspi_en": form.hsspi_en.data,
                    "lsspi_en": form.lsspi_en.data,
                    "wifi_en": form.wifi_en.data,
                    "wifi_smartconnect_en": form.smart_conn_en.data,
                    "wifi_reconnect_attempt": form.wifi_reconn.data,
                    "ssid1": form.ssid1.data,
                    "password1": form.password1.data,
                    "ssid2": form.ssid2.data,
                    "password2": form.password2.data,
                    "ssid3": form.ssid3.data,
                    "password3": form.password3.data,
                    "ssid4": form.ssid4.data,
                    "password4": form.password4.data,
                    "ssid5": form.ssid5.data,
                    "password5": form.password5.data,
                    "ssid6": form.ssid6.data,
                    "password6": form.password6.data,
                    "ssid7": form.ssid7.data,
                    "password7": form.password7.data,
                    "ssid8": form.ssid8.data,
                    "password8": form.password8.data,
                    "ssid9": form.ssid9.data,
                    "password9": form.password9.data,
                    "ssid10": form.ssid10.data,
                    "password10": form.password10.data,
                    "indicator_en": form.status_indicator_en.data,
                    "std_exception": form.std_exception_action.data,
                    "error_major": form.error_major_action.data,
                    "error_minor": form.error_minor_action.data,
                    "warn_major": form.warn_major_action.data,
                    "warn_minor": form.warn_minor_action.data
                })
            return True
        else:
            return False

    @staticmethod
    def update_form(form, device_uuid):
        dev_rec = device_db.find_one({'device_uuid': device_uuid, 'doc_type': 'system'})
        if dev_rec is not None:
            form.device_type.data = dev_rec["device_type"]
            form.device_uuid.data = dev_rec["device_uuid"]
            form.network_id.data = dev_rec["network_id"]
            form.description.data = dev_rec["description"]
            form.uart0_en.data = dev_rec["uart0_en"]
            form.uart0_baud.data = dev_rec["uart0_baud"]
            form.uart1_en.data = dev_rec["uart1_en"]
            form.uart1_baud.data = dev_rec["uart1_baud"]
            form.uart2_en.data = dev_rec["uart2_en"]
            form.uart2_baud.data = dev_rec["uart2_baud"]
            form.i2c0_en.data = dev_rec["i2c0_en"]
            form.i2c0_freq.data = dev_rec["i2c0_freq"]
            form.i2c1_en.data = dev_rec["i2c1_en"]
            form.i2c1_freq.data = dev_rec["i2c1_freq"]
            form.hsspi_en.data = dev_rec["hsspi_en"]
            form.lsspi_en.data = dev_rec["lsspi_en"]
            form.wifi_en.data = dev_rec["wifi_en"]
            form.smart_conn_en.data = dev_rec["wifi_smartconnect_en"]
            form.wifi_reconn.data = dev_rec["wifi_reconnect_attempt"]
            form.ssid1.data = dev_rec["ssid1"]
            form.password1.data = dev_rec["password1"]
            form.ssid2.data = dev_rec["ssid2"]
            form.password2.data = dev_rec["password2"]
            form.ssid3.data = dev_rec["ssid3"]
            form.password3.data = dev_rec["password3"]
            form.ssid4.data = dev_rec["ssid4"]
            form.password4.data = dev_rec["password4"]
            form.ssid5.data = dev_rec["ssid5"]
            form.password5.data = dev_rec["password5"]
            form.ssid6.data = dev_rec["ssid6"]
            form.password6.data = dev_rec["password6"]
            form.ssid7.data = dev_rec["ssid7"]
            form.password7.data = dev_rec["password7"]
            form.ssid8.data = dev_rec["ssid8"]
            form.password8.data = dev_rec["password8"]
            form.ssid9.data = dev_rec["ssid9"]
            form.password9.data = dev_rec["password9"]
            form.ssid10.data = dev_rec["ssid10"]
            form.password10.data = dev_rec["password10"]
            form.status_indicator_en.data = dev_rec["indicator_en"]
            form.std_exception_action.data = dev_rec["std_exception"]
            form.error_major_action.data = dev_rec["error_major"]
            form.error_minor_action.data = dev_rec["error_minor"]
            form.warn_major_action.data = dev_rec["warn_major"]
            form.warn_minor_action.data = dev_rec["warn_minor"]
            return True
        else:
            return False


# ==================== Protocol configuration page ==============================
class ProtocolForm(FlaskForm):
    device_uuid = StringField('Device UUID', render_kw={'readonly': True})
    mqtt_client_enable = BooleanField('Enable MQTT Client')
    mqtt_broker_uri = StringField('MQTT Client URI')
    mqtt_broker_port = StringField('MQTT Broker Port')
    keep_alive_timeout = StringField('Keep Alive Timeout')
    # add more parameters here

    save = SubmitField('Save')
    upload = SubmitField('Upload to device')


class ProtocolFormAttributes:
    @staticmethod
    def update_db(form):
        if form.device_uuid.data is not None:
            dev_rec = device_db.find_one({'device_uuid': form.device_uuid.data, 'doc_type': 'protocol'})
            if dev_rec is not None:
                # document with matching device id found
                dev_rec['device_uuid'] = form.device_uuid.data
                dev_rec['mqtt_client_enable'] = form.mqtt_client_enable.data
                dev_rec['mqtt_broker_uri'] = form.mqtt_broker_uri.data
                dev_rec['mqtt_broker_port'] = form.mqtt_broker_port.data
                dev_rec['keep_alive_timeout'] = form.keep_alive_timeout.data
                # add more parameters here

                device_db.save(dev_rec)
            else:
                # document with matching device id does not exists, so create new document in db
                device_db.insert({
                    'doc_type': 'protocol',
                    'device_uuid': form.device_uuid.data,
                    'mqtt_client_enable': form.mqtt_client_enable.data,
                    'mqtt_broker_uri': form.mqtt_broker_uri.data,
                    'mqtt_broker_port': form.mqtt_broker_port.data,
                    'keep_alive_timeout': form.keep_alive_timeout.data
                    # add more parameters here

                })
            return True
        else:
            return False

    @staticmethod
    def update_form(form, device_uuid):
        dev_rec = device_db.find_one({'device_uuid': device_uuid, 'doc_type': 'protocol'})
        if dev_rec is not None:
            form.device_uuid.data = dev_rec["device_uuid"]
            form.mqtt_client_enable.data = dev_rec["mqtt_client_enable"]
            form.mqtt_broker_uri.data = dev_rec["mqtt_broker_uri"]
            form.mqtt_broker_port.data = dev_rec['mqtt_broker_port']
            form.keep_alive_timeout.data = dev_rec['keep_alive_timeout']
            # add more parameters here

            return True
        else:
            return False


# ==================== Storage configuration page ==============================
class StorageForm(FlaskForm):
    device_uuid = StringField('Device UUID', render_kw={'readonly': True})
    # add more parameters here

    save = SubmitField('Save')
    upload = SubmitField('Upload to device')


class StorageFormAttributes:
    @staticmethod
    def update_db(form):
        if form.device_uuid.data is not None:
            dev_rec = device_db.find_one({'device_uuid': form.device_uuid.data, 'doc_type': 'storage'})
            if dev_rec is not None:
                # document with matching device id found
                dev_rec['device_uuid'] = form.device_uuid.data
                # add more parameters here

                device_db.save(dev_rec)
            else:
                # document with matching device id does not exists, so create new document in db
                device_db.insert({
                    'doc_type': 'storage',
                    'device_uuid': form.device_uuid.data,
                    # add more parameters here

                })
            return True
        else:
            return False

    @staticmethod
    def update_form(form, device_uuid):
        dev_rec = device_db.find_one({'device_uuid': device_uuid, 'doc_type': 'storage'})
        if dev_rec is not None:
            form.device_uuid.data = dev_rec["device_uuid"]
            # add more parameters here

            return True
        else:
            return False


# ==================== Sensor configuration page ==============================
class SensorForm(FlaskForm):
    device_uuid = StringField('Device UUID', render_kw={'readonly': True})
    # add more parameters here

    save = SubmitField('Save')
    upload = SubmitField('Upload to device')


class SensorFormAttributes:
    @staticmethod
    def update_db(form):
        if form.device_uuid.data is not None:
            dev_rec = device_db.find_one({'device_uuid': form.device_uuid.data, 'doc_type': 'sensor'})
            if dev_rec is not None:
                # document with matching device id found
                dev_rec['device_uuid'] = form.device_uuid.data
                # add more parameters here

                device_db.save(dev_rec)
            else:
                # document with matching device id does not exists, so create new document in db
                device_db.insert({
                    'doc_type': 'sensor',
                    'device_uuid': form.device_uuid.data,
                    # add more parameters here

                })
            return True
        else:
            return False

    @staticmethod
    def update_form(form, device_uuid):
        dev_rec = device_db.find_one({'device_uuid': device_uuid, 'doc_type': 'sensor'})
        if dev_rec is not None:
            form.device_uuid.data = dev_rec["device_uuid"]
            # add more parameters here

            return True
        else:
            return False