# Generated by Django 4.2 on 2023-06-14 12:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("mychatapp", "0003_message"),
    ]

    operations = [
        migrations.CreateModel(
            name="Image",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("image", models.ImageField(upload_to="img/%y")),
                ("nudity", models.BooleanField(default=False)),
                (
                    "img_reciver",
                    models.ForeignKey(
                        default="",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="img_reciver",
                        to="mychatapp.profile",
                    ),
                ),
                (
                    "img_sender",
                    models.ForeignKey(
                        default="",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="img_sender",
                        to="mychatapp.profile",
                    ),
                ),
            ],
        ),
    ]
