from django import forms
from .models import File


# form
class FileUploadForm(forms.Form):
    name = forms.CharField(label="名称", max_length=20,
                           widget=forms.TextInput(attrs={'class': 'form-control'}))
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))
    annotation = forms.CharField(label="备注", max_length=20,
                                 widget=forms.TextInput(attrs={'class': 'form-control'}))

    def clean_file(self):
        file = self.cleaned_data['file']
        # # 限制上传后缀
        # ext = file.name.split('.')[-1].lower()
        # if ext not in ["jpg", "pdf", "xlsx"]:
        #     raise forms.ValidationError("不支持的文件格式")
        return file


# Model form
class FileUploadModelForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ('name', 'file', 'annotation',)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'annotation': forms.TextInput(attrs={'class': 'form-control'}),
            'file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def clean_file(self):
        file = self.cleaned_data['file']
        # # 限制上传后缀
        # ext = file.name.split('.')[-1].lower()
        # if ext not in ["jpg", "pdf", "xlsx"]:
        #     raise forms.ValidationError("Only jpg, pdf and xlsx files are allowed.")
        # return cleaned data is very important.
        return file
