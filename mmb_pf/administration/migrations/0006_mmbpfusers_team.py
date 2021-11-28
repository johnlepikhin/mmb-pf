# Generated by Django 3.2.9 on 2021-11-27 13:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('addrbook', '0003_teams'),
        ('administration', '0005_mmbpfusers_images'),
    ]

    operations = [
        migrations.AddField(
            model_name='mmbpfusers',
            name='team',
            field=models.ForeignKey(help_text='Команда', null=True, on_delete=django.db.models.deletion.SET_NULL, to='addrbook.teams'),
        ),
    ]