from django.db import models
from django.contrib.auth.hashers import make_password
import os


# import os, uuid

class AdminUser(models.Model):
    """登录系统的账号密码"""
    username = models.CharField(verbose_name="用户名", max_length=32)
    password = models.CharField(verbose_name="密码", max_length=128)
    name = models.CharField(verbose_name="名称", max_length=32, null=True)

    def __str__(self):
        return self.username
    """重新配置password字段，使用pbkdf2加密算法保存"""
    def save(self, *args, **kwargs):
        self.password = make_password(self.password, None, 'pbkdf2_sha256')
        super(AdminUser, self).save(*args, **kwargs)

class AccountPassword(models.Model):
    """账号密码表"""
    name = models.CharField(verbose_name="名称", max_length=32)
    username = models.CharField(verbose_name="用户名", max_length=32)
    password = models.CharField(verbose_name="密码", max_length=128)
    note = models.CharField(verbose_name="备注", max_length=128, blank=True, null=True)

    def __str__(self):
        return self.username


class ServerInfo(models.Model):
    """主机信息表"""
    hostname = models.CharField(verbose_name="主机名", max_length=32)
    ipaddress = models.GenericIPAddressField(verbose_name="IP地址")
    platform_choices = (
        (1, "Liunx"),
        (2, "Windows"),
        (3, "MacOS"),
        (4, "Unix"),
        (5, "Other"),
    )
    platform = models.PositiveSmallIntegerField(verbose_name="平台", choices=platform_choices, default=1)
    protocol_choices = (
        (1, "ssh"),
        (2, "rdp"),
        (3, "telnet"),
        (4, "vnc"),
    )
    protocols = models.PositiveSmallIntegerField(verbose_name="协议", choices=protocol_choices, default=1)
    port = models.PositiveIntegerField(verbose_name="端口")
    note = models.CharField(verbose_name="备注", max_length=128)


def user_directory_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4().hex[:10], ext)
    return os.path.join("files", filename)
#
#
# class File(models.Model):
#     """文件信息"""
#     file = models.FileField(upload_to=user_directory_path, null=True)
#     upload_method = models.CharField(max_length=20, verbose_name="上传方法")
