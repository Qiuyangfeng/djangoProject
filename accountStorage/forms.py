from django import forms
from .models import AccountPassword
from django.conf import settings
import hashlib

def md5(data_string):
    obj = hashlib.md5(settings.SECRET_KEY.encode("utf-8"))
    obj.update(data_string.encode("utf-8"))
    return obj.hexdigest()

class Bootstrap():
    # password = forms.CharField(min_length=6, label="密码")
    def __init__ (self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for k, v in self.fields.items():
            if k == "create_time":
                v.widget.attrs = {"class": "form-control", "type": "text", "onclick": "WdatePicker({el:this,dateFmt:'yyyy-MM-dd'})", "placeholder": v.label}
                continue
            v.widget.attrs = {"class": "form-control", "placeholder": v.label}

class BootstrapModelForm(Bootstrap, forms.ModelForm):
    pass

class BootstrapForm(Bootstrap, forms.Form):
    pass

#######  modelform  #################

class UserModelForm(BootstrapModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = AccountPassword
        fields = ["name", "username", "password", "note"]

class LoginForm(BootstrapForm):
    username = forms.CharField(
        label="用户",
        widget=forms.TextInput,
        required=True
    )
    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput,
        required=True
    )
    code = forms.CharField(
        label="验证码",
        widget=forms.TextInput,
        required=True
    )

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)