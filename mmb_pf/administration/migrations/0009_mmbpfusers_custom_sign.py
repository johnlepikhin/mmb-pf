# Generated by Django 3.2.9 on 2021-11-27 15:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('addrbook', '0004_customsignes'),
        ('administration', '0008_mmbpfusers_sign'),
    ]

    operations = [
        migrations.AddField(
            model_name='mmbpfusers',
            name='custom_sign',
            field=models.ForeignKey(blank=True, help_text='Индивидуальный указатель', null=True, on_delete=django.db.models.deletion.SET_NULL, to='addrbook.customsignes'),
        ),
    ]