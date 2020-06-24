from application import device_db
from flask_wtf import FlaskForm


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
                # Anivnaash add more parameters here

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
                    # Anivnaash add more parameters here

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
            # Anivnaash add more parameters here

            return True
        else:
            return False


class SensorFormAttributes:
    @staticmethod
    def update_db(form):
        if form.device_uuid.data is not None:
            dev_rec = device_db.find_one({'device_uuid': form.device_uuid.data, 'doc_type': 'sensor'})
            if dev_rec is not None:
                # document with matching device id found
                dev_rec['device_uuid'] = form.device_uuid.data
                # Anivnaash add more parameters here

                device_db.save(dev_rec)
            else:
                # document with matching device id does not exists, so create new document in db
                device_db.insert({
                    'doc_type': 'sensor',
                    'device_uuid': form.device_uuid.data,
                    # Anivnaash add more parameters here

                })
            return True
        else:
            return False

    @staticmethod
    def update_form(form, device_uuid):
        dev_rec = device_db.find_one({'device_uuid': device_uuid, 'doc_type': 'sensor'})
        if dev_rec is not None:
            form.device_uuid.data = dev_rec["device_uuid"]
            # Anivnaash add more parameters here

            return True
        else:
            return False


class StorageFormAttributes:
    @staticmethod
    def update_db(form):
        if form.device_uuid.data is not None:
            dev_rec = device_db.find_one({'device_uuid': form.device_uuid.data, 'doc_type': 'storage'})
            if dev_rec is not None:
                # document with matching device id found
                dev_rec['device_uuid'] = form.device_uuid.data
                # Anivnaash add more parameters here

                device_db.save(dev_rec)
            else:
                # document with matching device id does not exists, so create new document in db
                device_db.insert({
                    'doc_type': 'storage',
                    'device_uuid': form.device_uuid.data,
                    # Anivnaash add more parameters here

                })
            return True
        else:
            return False

    @staticmethod
    def update_form(form, device_uuid):
        dev_rec = device_db.find_one({'device_uuid': device_uuid, 'doc_type': 'storage'})
        if dev_rec is not None:
            form.device_uuid.data = dev_rec["device_uuid"]
            # Anivnaash add more parameters here

            return True
        else:
            return False
