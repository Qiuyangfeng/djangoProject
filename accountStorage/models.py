from django.db import models
# from django.contrib.auth.hashers import make_password
from .untils.hash import md5
import os, uuid


# import os, uuid

class AdminUser(models.Model):
    """登录系统的账号密码"""
    username = models.CharField(verbose_name="用户名", max_length=32)
    password = models.CharField(verbose_name="密码", max_length=128)
    name = models.CharField(verbose_name="名称", max_length=32, blank=True, null=True)

    def __str__ (self):
        return self.username

    """重新配置password字段，使用md5或者pbkdf2加密算法保存"""

    def save (self, *args, **kwargs):
        self.password = md5(self.password)
        # self.password = make_password(self.password, None, 'pbkdf2_sha256')
        super(AdminUser, self).save(*args, **kwargs)


class AccountPassword(models.Model):
    """账号密码表"""
    name = models.CharField(verbose_name="名称", max_length=32, primary_key=False)
    username = models.CharField(verbose_name="用户名", max_length=32)
    password = models.CharField(verbose_name="密码", max_length=128)
    note = models.CharField(verbose_name="备注", max_length=128, blank=True, null=True)

    def __str__ (self):
        return self.username


class ServerInfo(models.Model):
    """主机信息表"""
    hostname = models.CharField(verbose_name="主机名", max_length=32, primary_key=True)
    ipaddress = models.GenericIPAddressField(verbose_name="IP地址")
    platform_choices = (
        ("Liunx", "Liunx"),
        ("Windows", "Windows"),
        ("MacOS", "MacOS"),
        ("Unix", "Unix"),
        ("Other", "Other"),
    )
    platform = models.CharField(verbose_name="平台", max_length=32, choices=platform_choices, default="Linux")
    protocol_choices = (
        ("ssh", "ssh"),
        ("rdp", "rdp"),
        ("telnet", "telnet"),
        ("vnc", "vnc"),
    )
    protocols = models.CharField(verbose_name="协议", max_length=32, choices=protocol_choices, default="ssh")
    port = models.PositiveIntegerField(verbose_name="端口")
    credentials = models.ForeignKey(verbose_name="账户凭证", to=AccountPassword, on_delete=models.SET_NULL, blank=True,
                                    null=True)
    note = models.CharField(verbose_name="备注", max_length=128, blank=True, null=True)


def user_directory_path (instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4().hex[:10], ext)
    return os.path.join("files", filename)
#
#
# class File(models.Model):
#     """文件信息"""
#     file = models.FileField(upload_to=user_directory_path, null=True)
#     upload_method = models.CharField(max_length=20, verbose_name="上传方法")
