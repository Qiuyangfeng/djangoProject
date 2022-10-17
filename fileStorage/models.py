# import os
# import uuid
from django.db import models


# def user_directory_path(instance, filename):
#     """定义路径名"""
#     ext = filename.split('.')[-1]
#     filename = '{}.{}'.format(uuid.uuid4().hex[:10], ext)
#     return os.path.join("files", filename)


class File(models.Model):
    """文件信息"""
    name = models.CharField(max_length=20, verbose_name="自定义名")
    file = models.FileField(upload_to="media/%Y-%M-%D", null=True, verbose_name="文件路径")
    # file = models.FileField(upload_to=user_directory_path, null=True, verbose_name="文件路径")
    annotation = models.CharField(max_length=20, verbose_name="备注")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="上传时间")
