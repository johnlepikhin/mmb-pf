# Generated by Django 3.2.9 on 2021-11-22 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0004_imagestorage'),
    ]

    operations = [
        migrations.AddField(
            model_name='mmbpfusers',
            name='images',
            field=models.ManyToManyField(blank=True, related_name='user_images', to='administration.ImageStorage'),
        ),
    ]
