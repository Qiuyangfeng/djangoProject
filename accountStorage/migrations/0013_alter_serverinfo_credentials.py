# Generated by Django 4.1.1 on 2022-11-23 03:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accountStorage', '0012_remove_serverinfo_name_serverinfo_credentials'),
    ]

    operations = [
        migrations.AlterField(
            model_name='serverinfo',
            name='credentials',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accountStorage.accountpassword', verbose_name='账户凭证'),
        ),
    ]
