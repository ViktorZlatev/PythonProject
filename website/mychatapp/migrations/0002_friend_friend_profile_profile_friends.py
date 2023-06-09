# Generated by Django 4.1.7 on 2023-04-22 15:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mychatapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='friend',
            name='friend_profile',
            field=models.OneToOneField(default='', on_delete=django.db.models.deletion.CASCADE, to='mychatapp.profile'),
        ),
        migrations.AddField(
            model_name='profile',
            name='friends',
            field=models.ManyToManyField(to='mychatapp.friend'),
        ),
    ]
