from flask import flash, redirect
from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, BooleanField, SubmitField, PasswordField, RadioField, TextAreaField
from wtforms.validators import DataRequired
from flask_app import device_db


class DeviceStatusForm(FlaskForm):
    config_modules = ['Dashboard', 'Operational']
    deviceID = StringField('Device ID', validators=[DataRequired(message='Please enter device ID')])
    configuration = RadioField('Select configuration module',
                               choices=config_modules, default='Dashboard')
    next = SubmitField('Next')


class DeviceStatusDashboardForm(FlaskForm):
    device_uuid = StringField('Device UUID', render_kw={'readonly': True})
    add_dashboard_name = StringField('Name')
    add_dashboard_url = StringField('URL')
    add_dashboard = SubmitField('Add')
    rm_select_dashboard = SelectField('Remove')
    rm_dashboard = SubmitField('Remove')
    select_dashboard = SelectField('Dashboard')
    view_dashboard = SubmitField('View')


class DeviceStatusDashboardFormAttributes:
    @staticmethod
    def update_db(form):
        if form.device_uuid.data is not None:
            dev_rec = device_db.find_one({'device_uuid': form.device_uuid.data, 'doc_type': 'dashboard'})
            if dev_rec is not None:
                # append new URL based on unique short name
                temp_dashboard_list = dev_rec['dashboard_collection']
                duplicate = False
                for item in temp_dashboard_list:
                    if form.add_dashboard_name.data in item:
                        duplicate = True
                        break;
                if not duplicate:
                    temp_dashboard_list.append((form.add_dashboard_url.data, form.add_dashboard_name.data))
                    dev_rec['dashboard_collection'] = temp_dashboard_list

                device_db.save(dev_rec)
            else:
                # document with matching device id does not exists, so create new document in db
                device_db.insert({
                    'doc_type': 'dashboard',
                    'device_uuid': form.device_uuid.data,
                    'dashboard_collection': []
                })
            return True
        else:
            return False

    @staticmethod
    def update_form(form, device_uuid):
        dev_rec = device_db.find_one({'device_uuid': device_uuid, 'doc_type': 'dashboard'})
        if dev_rec is not None:
            form.device_uuid.data = dev_rec["device_uuid"]
            dashboard_list = dev_rec["dashboard_collection"]
            form.select_dashboard.choices = dashboard_list
            form.rm_select_dashboard.choices = dashboard_list
            return True
        else:
            return False
