# Generated by Django 4.1 on 2022-10-25 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fileStorage', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='annotation',
            field=models.CharField(max_length=20, null=True, verbose_name='备注'),
        ),
        migrations.AlterField(
            model_name='file',
            name='file',
            field=models.FileField(null=True, upload_to='media/%Y-%m-%d', verbose_name='文件路径'),
        ),
    ]
