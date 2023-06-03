# Generated by Django 4.1.7 on 2023-06-01 05:29

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("network", "0006_addpost_like"),
    ]

    operations = [
        migrations.AlterField(
            model_name="addpost",
            name="like",
            field=models.ManyToManyField(
                blank=True, related_name="like", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
