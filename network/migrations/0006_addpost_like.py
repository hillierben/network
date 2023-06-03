# Generated by Django 4.1.7 on 2023-06-01 05:28

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("network", "0005_delete_like"),
    ]

    operations = [
        migrations.AddField(
            model_name="addpost",
            name="like",
            field=models.ManyToManyField(
                related_name="like", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
