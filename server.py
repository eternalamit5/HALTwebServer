from flask_mail import Message
from flask import Flask, request, jsonify, render_template, session, redirect, flash, abort, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import settings
from login_registration import LoginForm, RegistrationForm
from device_config import DeviceConfigurationForm, SystemForm, ProtocolForm, SensorForm, StorageForm, \
    SystemFormAttributes, ProtocolFormAttributes, SensorFormAttributes, StorageFormAttributes
from device_status import DeviceStatusForm, DeviceStatusDashboardForm, DeviceStatusDashboardFormAttributes
from mqtt_client import MqttClientAppForm
import json
from bson.json_util import dumps, loads
from flask_app import app, mongo, user_db, device_db, mail, flask_mqtt_client


# >>>>>>> Login, logout, register <<<<<<<<<<<<<<


@app.route("/", methods=["GET"])
def root_route():
    '''
    Method redirects to login page
    :return:
    '''
    return redirect('/login')


@app.route("/login", methods=["GET", "POST"])
def login_route():
    '''
    Method implementing login form
    Get request directs login page
    Post request directs to
        home page on successful login
        login page on fail to login
    :return:
    '''
    if request.method == "GET":
        form = LoginForm()
        return render_template('login.html', form=form)
    else:
        form = LoginForm()
        if form.validate_on_submit():
            if form.forgot_password.data:
                usr_rec = user_db.find_one({'username': form.username.data.lower()})
                print(usr_rec['e-mail'])
                if usr_rec is not None:
                    msg = Message('Uptime registration <Do not reply>', recipients=list(usr_rec['password']))
                    msg.body = f"Your login username {form.username.data} and password {usr_rec['password']}"
                    mail.send(msg)
                else:
                    flash(f'Username does not exits in database')
                    return render_template('register.html', form=form)
            else:
                # check if user exists in db
                usr_rec = user_db.find_one({'username': form.username.data.lower()})
                if usr_rec is not None:

                    # user exists in db, validate password
                    if check_password_hash(usr_rec['password'], form.password.data):

                        # user password matching, so start permanent session for the user
                        session.permanent = True
                        session["user"] = form.username

                        # flash welcome message to the user
                        flash('Welcome ' + form.username.data + ' !!!')

                        # redirect to home page
                        return redirect('/home')
                    else:
                        # Password is not matching
                        flash('Invalid Password !. Password is case sensitive')
                        return redirect('/login')
                else:
                    # fail to login redirect to login page
                    flash('Username does not exists, try again !')
                    return redirect('/login')

        # Form not validated
        return redirect('login.html')


@app.route("/logout", methods=["GET"])
def logout_route():
    '''
    method logouts by ending the user session
    redirects to login page
    :return:
    '''
    session.pop("user", None)
    return redirect('/login')


@app.route("/register", methods=["GET", "POST"])
def register_route():
    '''
    method registers new user by adding to the database
    registration fails if username already exists and redirects to registration page
    registration succeeds if unique username is expected and redirects to home page
    :return:
    '''
    if request.method == "GET":
        form = RegistrationForm()
        return render_template("register.html", form=form)
    else:
        form = RegistrationForm()
        if form.validate_on_submit():
            usr_rec = user_db.find_one({'username': form.username.data.lower()})
            # match confirm password and password
            if form.password.data != form.confirm_password.data:
                new_form = RegistrationForm()
                new_form.username.data = form.username.data
                new_form.email.data = form.email.data
                flash('password and confirm password not matching')
                return render_template('register.html', form=new_form)

            # find if username is found unique in the db
            usr_rec = user_db.find_one({'username': form.username.data.lower()})
            if usr_rec is None:
                #  add new user name and password to the db
                user_db.insert({'username': form.username.data.lower(),
                                'password': generate_password_hash(form.password.data),
                                'e-mail': form.email.data
                                })

                session.permanent = True
                session["user"] = form.username
                flash('Welcome ' + form.username.data + ' !!!')
                flash('You have successful registered with our platform ')
                return redirect('/home')
            else:
                new_form = RegistrationForm()
                new_form.username.data = form.username.data
                new_form.email.data = form.email.data
                flash('Username already exists, try other username !!!')
                return render_template('register.html', form=new_form)
        else:
            return redirect('/home')


# >>>>>>> About and home page <<<<<<<<<<<<<<


@app.route("/about", methods=["GET"])
def about_route():
    '''
    method shows about page if user session is running
    else redirects to login page
    :return:
    '''
    if "user" in session:
        user = session["user"]
        return render_template("about.html")
    else:
        return redirect('/login')


@app.route("/home", methods=["GET"])
def home_route():
    '''
    method shows home page if user session is running
    else redirects to login page
    :return:
    '''
    uri = "www.google.com"
    if "user" in session:
        user = session["user"]
        return render_template("home.html")
    else:
        return redirect('/login')


# >>>>>>> Device status page <<<<<<<<<<<<<<

@app.route("/device_status", methods=["GET", "POST"])
def device_status_route():
    '''
    method implements device status form
    Get request shows the device status if user session is running
    else directs to login page
    :return:
    '''
    if request.method == "GET":
        # check if user session is running
        if "user" in session:
            user = session["user"]

            # create device Status form object
            form = DeviceStatusForm()
            return render_template("device_status.html", form=form)
        else:
            return redirect('/login')
    else:
        # check if user session is running
        if "user" in session:
            user = session["user"]
            form = DeviceStatusForm()

            if form.is_submitted():
                if form.configuration.data == "Dashboard":
                    return redirect("/device_status/dashboard/" + form.deviceID.data)
                elif form.configuration.data == "Operational":
                    return redirect("/device_status/oper_status/" + form.deviceID.data)


@app.route("/device_status/dashboard/<path:devid>", methods=["GET", "POST"])
def device_status_dashboard_route(devid):
    '''
    method implements device status form
    Get request shows the device status if user session is running
    else directs to login page
    :return:
    '''
    if request.method == "GET":
        # check if user session is running
        if "user" in session:
            user = session["user"]

            # create device Status form object
            form = DeviceStatusDashboardForm()

            # check if device id already exists in db
            dev_rec = device_db.find_one({'device_uuid': devid, 'doc_type': 'dashboard'})
            if dev_rec is None:
                form.device_uuid.data = devid
                DeviceStatusDashboardFormAttributes.update_db(form)
            else:
                DeviceStatusDashboardFormAttributes.update_form(form, devid)
            return render_template("dashboard.html", form=form)
        else:
            return redirect('/login')
    else:
        # check if user session is running
        if "user" in session:
            user = session["user"]
            form = DeviceStatusDashboardForm()

            if form.is_submitted():
                if form.add_dashboard.data:
                    new_form = DeviceStatusDashboardForm()
                    if DeviceStatusDashboardFormAttributes.update_db(form):
                        if DeviceStatusDashboardFormAttributes.update_form(new_form,devid):
                            new_form.select_dashboard.data = form.select_dashboard.data
                            new_form.add_dashboard_name.data = form.add_dashboard_name.data
                            new_form.add_dashboard_url.data = form.add_dashboard_url.data
                            return render_template("dashboard.html", form=new_form, show_url="", show=False)
                    flash(f'Failed to Update dashboard')
                    return redirect("/device_status/dashboard")

                elif form.view_dashboard.data:
                    show_url = ""
                    dev_rec = device_db.find_one({'device_uuid': devid, 'doc_type': 'dashboard'})
                    if dev_rec is not None:
                        dashboard_list = dev_rec["dashboard_collection"]
                        for item in dashboard_list:
                            if form.select_dashboard.data in item:
                                show_url = item[0]
                                break
                    new_form = DeviceStatusDashboardForm()
                    if DeviceStatusDashboardFormAttributes.update_form(new_form, devid):
                        new_form.select_dashboard.data = form.select_dashboard.data
                        return render_template("dashboard.html", form=new_form, show_url=show_url, show=True)
                    flash(f'Failed to View dashboard')
                    return redirect("/device_status/dashboard/"+devid)

                elif form.rm_dashboard.data:
                    dev_rec = device_db.find_one({'device_uuid': devid, 'doc_type': 'dashboard'})
                    if dev_rec is not None:
                        dashboard_list = dev_rec["dashboard_collection"]
                        for item in dashboard_list:
                            if form.rm_select_dashboard.data in item:
                                dashboard_list.remove(item)
                                dev_rec['dashboard_collection'] = dashboard_list
                                device_db.save(dev_rec)
                                return redirect("/device_status/dashboard/" + devid)
            else:
                return redirect('/home')
        else:
            return redirect('/login')


# >>>>>>> Device configuration <<<<<<<<<<<<<<
@app.route("/device_config", methods=["GET", "POST"])
def device_config_route():
    '''
    method implements device configuration menu
    Using this menu we specific device's configuration based on device ID
    GET request loads device configuration menu page
    POST request validates the choices and redirects to respective page
        system configuration page
        sensor configuration page
        protocol configuration page
        storage configuration page
    Any failure will redirect to device configuration menu page
    :return:
    '''
    if request.method == "GET":
        if "user" in session:
            user = session["user"]

            # create device configuration form
            form = DeviceConfigurationForm()
            return render_template("device_config.html", form=form)
        else:
            return redirect('/login')
    else:
        form = DeviceConfigurationForm()
        if form.is_submitted():
            if not form.new_device.data:
                # check if device id already exists in db
                dev_rec = device_db.find_one({'device_uuid': form.deviceID.data})
                if dev_rec is None:
                    # Its not a new device and its device id not found in db
                    new_form = DeviceConfigurationForm()
                    new_form.configuration.data = form.configuration.data
                    flash(f"Device with ID = {form.deviceID.data} does not exists")
                    return render_template("device_config.html", form=form)

            if form.configuration.data == 'System':
                return redirect('/devconfig/system/device/' + form.deviceID.data)
            elif form.configuration.data == 'Sensor':
                return redirect('/devconfig/sensor/device/' + form.deviceID.data)
            elif form.configuration.data == 'Protocol':
                return redirect('/devconfig/protocol/device/' + form.deviceID.data)
            elif form.configuration.data == 'Storage':
                return redirect('/devconfig/storage/device/' + form.deviceID.data)
            else:
                return redirect('/device_config')

    return redirect('/device_config')


# Path: /devconfig/system/device/<device_id>
@app.route("/devconfig/system/device/<path:devid>", methods=["GET", "POST"])
def system_config_route(devid):
    '''
    method implements system configuration page
    :param devid: device id of the device resquesting the configuration
    :return:
    '''
    if request.method == "GET":
        # check if user is in current session
        if "user" in session:
            user = session["user"]
            # create SystemForm object
            form = SystemForm()
            # Find document with matching device_uuid
            dev_rec = device_db.find_one({'device_uuid': devid, 'doc_type': 'system'})
            if dev_rec is None:
                # no matching document found
                # update form with device ID
                form.device_uuid.data = devid
                # update db with using form attributes
                if not SystemFormAttributes.update_db(form):
                    flash(f"System configuration failed")
                    return redirect('/device_config')
            # update form with attributes from db with matching device uuid
            if SystemFormAttributes.update_form(form, devid):
                return render_template("system.html", form=form)
            else:
                flash(f"System configuration failed")
                return redirect('/device_config')
        else:
            return redirect('/login')

    elif request.method == 'POST':
        form = SystemForm()
        if form.is_submitted():
            # if save button is pressed
            if form.save.data is True:
                # update the data in db
                dev_rec = device_db.find_one({'device_uuid': devid, 'doc_type': 'system'})
                if dev_rec is not None:
                    # update db with using form attributes
                    if not SystemFormAttributes.update_db(form):
                        flash(f"System configuration failed")
                        return redirect('/device_config')
                    else:
                        flash('System configurations saved successfully')
                        return redirect('/device_config')
                else:
                    flash(f'System configurations Failed, device with ID {devid} does not exists in DB')
                    return redirect('/device_config')
            # upload button pressed
            elif form.upload.data is True:
                # update the data in db
                dev_rec = device_db.find_one({'device_uuid': devid, 'doc_type': 'system'})
                if dev_rec is not None:
                    # update db with using form attributes
                    if not SystemFormAttributes.update_db(form):
                        flash(f"System configuration failed")
                        return redirect('/device_config')
                    else:
                        # todo send message to the device to reboot using mqtt client
                        flash('System configurations saved successfully')
                        return redirect('/device_config')
                else:
                    flash(f'System configurations Failed, device with ID {devid} does not exists in DB')
                    return redirect('/device_config')

    return redirect('/devconfig/system/device/' + devid)


# Path: /devconfig/protocol/device/<device_id>
@app.route("/devconfig/protocol/device/<path:devid>", methods=["GET", "POST"])
def protocol_config_route(devid):
    if request.method == "GET":
        # check if user is in current session
        if "user" in session:
            user = session["user"]
            # create SystemForm object
            form = ProtocolForm()
            # Find document with matching device_uuid
            dev_rec = device_db.find_one({'device_uuid': devid, 'doc_type': 'protocol'})
            if dev_rec is None:
                # no matching document found
                # update form with device ID
                form.device_uuid.data = devid
                # update db with using form attributes
                if not ProtocolFormAttributes.update_db(form):
                    flash(f"Protocol configuration failed")
                    return redirect('/device_config')
            # update form with attributes from db with matching device uuid
            if ProtocolFormAttributes.update_form(form, devid):
                return render_template("protocol.html", form=form)
            else:
                flash(f"Protocol configuration failed")
                return redirect('/device_config')
        else:
            return redirect('/login')

    elif request.method == 'POST':
        form = ProtocolForm()
        if form.is_submitted():
            # if save button is pressed
            if form.save.data is True:
                # update the data in db
                dev_rec = device_db.find_one({'device_uuid': devid, 'doc_type': 'protocol'})
                if dev_rec is not None:
                    # update db with using form attributes
                    if not ProtocolFormAttributes.update_db(form):
                        flash(f"Protocol configuration failed")
                        return redirect('/device_config')
                    else:
                        flash('Protocol configurations saved successfully')
                        return redirect('/device_config')
                else:
                    flash(f'Protocol configurations Failed, device with ID {devid} does not exists in DB')
                    return redirect('/device_config')
            # upload button pressed
            elif form.upload.data is True:
                # update the data in db
                dev_rec = device_db.find_one({'device_uuid': devid, 'doc_type': 'protocol'})
                if dev_rec is not None:
                    # update db with using form attributes
                    if not ProtocolFormAttributes.update_db(form):
                        flash(f"Protocol configuration failed")
                        return redirect('/device_config')
                    else:
                        # todo send message to the device to reboot using mqtt client
                        flash('Protocol configurations saved successfully')
                        return redirect('/device_config')
                else:
                    flash(f'Protocol configurations Failed, device with ID {devid} does not exists in DB')
                    return redirect('/device_config')

    return redirect('/devconfig/protocol/device/' + devid)


# Path: /devconfig/sensor/device/<device_id>
@app.route("/devconfig/sensor/device/<path:devid>", methods=["GET", "POST"])
def sensor_config_route(devid):
    if request.method == "GET":
        # check if user is in current session
        if "user" in session:
            user = session["user"]
            # create SystemForm object
            form = SensorForm()
            # Find document with matching device_uuid
            dev_rec = device_db.find_one({'device_uuid': devid, 'doc_type': 'sensor'})
            if dev_rec is None:
                # no matching document found
                # update form with device ID
                form.device_uuid.data = devid
                # update db with using form attributes
                if not SensorFormAttributes.update_db(form):
                    flash(f"Sensor configuration failed")
                    return redirect('/device_config')
            # update form with attributes from db with matching device uuid
            if SensorFormAttributes.update_form(form, devid):
                return render_template("sensor.html", form=form)
            else:
                flash(f"Sensor configuration failed")
                return redirect('/device_config')
        else:
            return redirect('/login')

    elif request.method == 'POST':
        form = SensorForm()
        if form.is_submitted():
            # if save button is pressed
            if form.save.data is True:
                # update the data in db
                dev_rec = device_db.find_one({'device_uuid': devid, 'doc_type': 'sensor'})
                if dev_rec is not None:
                    # update db with using form attributes
                    if not SensorFormAttributes.update_db(form):
                        flash(f"Sensor configuration failed")
                        return redirect('/device_config')
                    else:
                        flash('Sensor configurations saved successfully')
                        return redirect('/device_config')
                else:
                    flash(f'Sensor configurations Failed, device with ID {devid} does not exists in DB')
                    return redirect('/device_config')
            # upload button pressed
            elif form.upload.data is True:
                # update the data in db
                dev_rec = device_db.find_one({'device_uuid': devid, 'doc_type': 'sensor'})
                if dev_rec is not None:
                    # update db with using form attributes
                    if not SensorFormAttributes.update_db(form):
                        flash(f"Sensor configuration failed")
                        return redirect('/device_config')
                    else:
                        # todo send message to the device to reboot using mqtt client
                        flash('Sensor configurations saved successfully')
                        return redirect('/device_config')
                else:
                    flash(f'Sensor configurations Failed, device with ID {devid} does not exists in DB')
                    return redirect('/device_config')

    return redirect('/devconfig/sensor/device/' + devid)


# Path: /devconfig/storage/device/<device_id>
@app.route("/devconfig/storage/device/<path:devid>", methods=["GET", "POST"])
def storage_config_route(devid):
    if request.method == "GET":
        # check if user is in current session
        if "user" in session:
            user = session["user"]
            # create SystemForm object
            form = StorageForm()
            # Find document with matching device_uuid
            dev_rec = device_db.find_one({'device_uuid': devid, 'doc_type': 'storage'})
            if dev_rec is None:
                # no matching document found
                # update form with device ID
                form.device_uuid.data = devid
                # update db with using form attributes
                if not StorageFormAttributes.update_db(form):
                    flash(f"Storage configuration failed")
                    return redirect('/device_config')
            # update form with attributes from db with matching device uuid
            if StorageFormAttributes.update_form(form, devid):
                return render_template("storage.html", form=form)
            else:
                flash(f"Storage configuration failed")
                return redirect('/device_config')
        else:
            return redirect('/login')

    elif request.method == 'POST':
        form = StorageForm()
        if form.is_submitted():
            # if save button is pressed
            if form.save.data is True:
                # update the data in db
                dev_rec = device_db.find_one({'device_uuid': devid, 'doc_type': 'storage'})
                if dev_rec is not None:
                    # update db with using form attributes
                    if not StorageFormAttributes.update_db(form):
                        flash(f"Storage configuration failed")
                        return redirect('/device_config')
                    else:
                        flash('Storage configurations saved successfully')
                        return redirect('/device_config')
                else:
                    flash(f'Storage configurations Failed, device with ID {devid} does not exists in DB')
                    return redirect('/device_config')
            # upload button pressed
            elif form.upload.data is True:
                # update the data in db
                dev_rec = device_db.find_one({'device_uuid': devid, 'doc_type': 'storage'})
                if dev_rec is not None:
                    # update db with using form attributes
                    if not StorageFormAttributes.update_db(form):
                        flash(f"Storage configuration failed")
                        return redirect('/device_config')
                    else:
                        # todo send message to the device to reboot using mqtt client
                        flash('Storage configurations saved successfully')
                        return redirect('/device_config')
                else:
                    flash(f'Storage configurations Failed, device with ID {devid} does not exists in DB')
                    return redirect('/device_config')

    return redirect("/devconfig/storage/device/" + devid)


# Path: /mqtt/client/app
@app.route("/mqtt/client/app", methods=["POST", "GET"])
def mqttclient_app_route():
    if request.method == "GET":
        if "user" in session:
            user = session["user"]
            form = MqttClientAppForm()
            form.is_client_connected = flask_mqtt_client.get_status()
            return render_template("mqttclientapp.html", form=form)
        else:
            return redirect('/login')
    else:
        form = MqttClientAppForm()
        if form.is_submitted():
            if form.pub_add.data:
                if flask_mqtt_client.add_publish_topic(form.pub_topic_add.data):
                    pass
                else:
                    pass
            if form.sub_add.data:
                if flask_mqtt_client.add_subscription_topic(form.sub_topic_add.data):
                    pass
                else:
                    pass
            if form.pub_rm.data:
                if flask_mqtt_client.rm_publish_topic(form.pub_topic_rm.data):
                    pass
                else:
                    pass
            if form.sub_rm.data:
                if flask_mqtt_client.rm_subscription_topic(form.pub_topic_rm.data):
                    pass
                else:
                    pass
            if form.send.data:
                if flask_mqtt_client.on_message_send(form.pub_topic.data, form.pub_data.data, form.pub_qos_add.data):
                    pass
                else:
                    flash(f'Message failed to send')

            new_form = MqttClientAppForm()
            new_form.pub_topic_rm.data = flask_mqtt_client.mqttclient_pub_topic_list
            new_form.pub_topic.data = flask_mqtt_client.mqttclient_pub_topic_list
            new_form.sub_topic_rm.data = flask_mqtt_client.mqttclient_sub_topic_list
            new_form.is_client_connected = flask_mqtt_client.get_status()
            return render_template("mqttclientapp.html", form=new_form)
        else:
            return redirect('/home')


@app.route("/mqtt/client/app/update/log", methods=["GET"])
def mqttclient_updatelog_route():
    ret = flask_mqtt_client.update()
    if ret is not None:
        return ret
    return ''


@app.route("/download/device/config", methods=["POST"])
def download_dev_config():
    json1_data = json.loads(request.get_data())
    username = json1_data['username']
    password = json1_data['password']
    device_id = json1_data['device_id']
    config_item = json1_data['doc_type']
    if username is not None and password is not None and device_id is not None and config_item is not None:
        usr_rec = user_db.find_one({'username': username.lower()})
        if usr_rec is not None:
            # user exists in db, validate password
            if check_password_hash(usr_rec['password'], password):
                dev_rec = device_db.find_one({'device_uuid': device_id, 'doc_type': config_item})
                if dev_rec is not None:
                    return dumps(dev_rec)
    return '''{"doc_type"="None"}'''


if __name__ == '__main__':
    app.run(debug=True, port=1515, host='0.0.0.0')
