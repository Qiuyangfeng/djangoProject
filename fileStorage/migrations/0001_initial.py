# Generated by Django 4.1.1 on 2022-10-17 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='自定义名')),
                ('file', models.FileField(null=True, upload_to='media/%Y-%M-%D', verbose_name='文件路径')),
                ('annotation', models.CharField(max_length=20, verbose_name='备注')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='上传时间')),
            ],
        ),
    ]