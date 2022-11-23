# Generated by Django 4.1.1 on 2022-11-23 02:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accountStorage', '0009_serverinfo_name_alter_serverinfo_platform_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='serverinfo',
            name='platform',
            field=models.CharField(choices=[('Liunx', 'Liunx'), ('Windows', 'Windows'), ('MacOS', 'MacOS'), ('Unix', 'Unix'), ('Other', 'Other')], default='Linux', max_length=32, verbose_name='平台'),
        ),
        migrations.AlterField(
            model_name='serverinfo',
            name='protocols',
            field=models.CharField(choices=[('ssh', 'ssh'), ('rdp', 'rdp'), ('telnet', 'telnet'), ('vnc', 'vnc')], default='ssh', max_length=32, verbose_name='协议'),
        ),
    ]
