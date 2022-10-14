from accountStorage import models
from accountStorage.untils.bootstrap import BootstrapModelForm

#######  modelform  #################

class UserModelForm(BootstrapModelForm):
    class Meta:
        model = models.AccountPassword
        fields = ["name", "username", "password", "note"]
