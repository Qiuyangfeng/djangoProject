from django import forms
from .models import File,AccountPassword

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
    class Meta:
        model = AccountPassword
        fields = ["name", "username", "password", "note"]

class FileUploadForm(forms.Form):
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))
    upload_method = forms.CharField(label="上传方法", max_length=20,
                                    widget=forms.TextInput(attrs={'class': 'form-control'}))
    def clean_file(self):
        file = self.cleaned_data['file']
        ext = file.name.split('.')[-1].lower()
        if ext not in ["jpg", "pdf", "xlsx"]:
            raise forms.ValidationError("不支持的文件格式")
        return file

# Model form
class FileUploadModelForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ('file', 'upload_method',)
        widgets = {
            'upload_method': forms.TextInput(attrs={'class': 'form-control'}),
            'file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def clean_file(self):
        file = self.cleaned_data['file']
        ext = file.name.split('.')[-1].lower()
        if ext not in ["jpg", "pdf", "xlsx"]:
            raise forms.ValidationError("Only jpg, pdf and xlsx files are allowed.")
        # return cleaned data is very important.
        return file