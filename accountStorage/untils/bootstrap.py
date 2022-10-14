from django import forms

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

