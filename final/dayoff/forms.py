from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core import validators
from dayoff.models import Dayoff
import datetime

class EmployeeForm(forms.Form):
    firstname = forms.CharField(required=True, label="Firstname")
    lastname = forms.CharField(required=True, label="Lastname")
    email = forms.CharField(required=True, validators=[validators.validate_email], label="Email")
    username = forms.CharField(required=True, label="Username")
    password1 = forms.CharField(required=True, label="Password")
    password2 = forms.CharField(required=True, label="Confirm Password")

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 is not None and password2 is not None:
            if len(password1) < 8:
                self.add_error('password1', 'Password must be longer than 8')
            else:
                if password1 != password2:
                    self.add_error('password2', 'Please Confirm Password Correctly')

        if username is not None:
            if len(username) < 8:
                self.add_error('username', 'Username must be longer than 8')

class LoginForm(forms.Form):
    username = forms.CharField(required=True, label="Username")
    password = forms.CharField(required=True, label="Password")

    def clean_username(self):
        username = self.cleaned_data['username']
        if username is not None:
            if len(username) < 8:
                raise forms.ValidationError('Please Enter Username Correctly')

        return username

class leaveRequestForm(forms.Form):
    reason = forms.CharField(required=True, label="เนื่องจาก", widget=forms.Textarea())
    type = forms.ChoiceField(required=True, widget=forms.RadioSelect,choices=Dayoff.TYPES, label="ประเภท")
    start_date = forms.DateField(required=True, widget=forms.SelectDateWidget())
    end_date = forms.DateField(required=True, widget=forms.SelectDateWidget())

    def clean(self):
        data = super().clean()

        start = data.get('date_start')
        end = data.get('date_end')

        if start is None or end is None:
            raise forms.ValidationError('กรุณาเลือกระยะเวลา')

        elif start > end:
            raise forms.ValidationError('วันสิ้นสุดต้องเป็นวันที่หลังจากวันเริ่มต้น')
        elif start < datetime.datetime.now().date():
            raise forms.ValidationError('ไม่สามารถเลือกวันที่ในอดีตได้')


