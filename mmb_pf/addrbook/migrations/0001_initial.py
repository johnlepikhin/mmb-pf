# Generated by Django 3.2.9 on 2021-11-22 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='StreetSignes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', help_text='Название знака', max_length=512, unique=True)),
            ],
            options={
                'verbose_name_plural': 'Уличные указатели',
            },
        ),
    ]