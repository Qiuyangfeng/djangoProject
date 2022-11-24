from django import forms
from accountStorage.models import AccountPassword, ServerInfo
from accountStorage.untils.hash import md5


class Bootstrap():
    # password = forms.CharField(min_length=6, label="密码")
    def __init__ (self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for k, v in self.fields.items():
            if k == "create_time":
                v.widget.attrs = {"class": "form-control", "type": "text",
                                  "onclick": "WdatePicker({el:this,dateFmt:'yyyy-MM-dd'})", "placeholder": v.label}
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


class ServerModelForm(BootstrapModelForm):
    class Meta:
        model = ServerInfo
        fields = "__all__"


class LoginForm(BootstrapForm):
    username = forms.CharField(
        label="用户名",
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

    def clean_password (self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)
        # return pbkdf2(pwd)


class RegisterFrom(BootstrapForm):
    register_username = forms.CharField(
        label="用户名",
        widget=forms.TextInput,
        required=True
    )
    register_password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput,
        required=True
    )

    confirm_password = forms.CharField(
        label="重复密码",
        widget=forms.PasswordInput,
        required=True
    )
