# Generated by Django 4.1.7 on 2023-06-05 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mychatapp', '0003_message'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='img/%y')),
            ],
        ),
    ]
