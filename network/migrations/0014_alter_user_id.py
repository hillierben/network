# Generated by Django 4.1.7 on 2023-06-03 11:35

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("network", "0013_remove_follow_follows_alter_like_post_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="id",
            field=models.UUIDField(editable=False, primary_key=True, serialize=False),
        ),
    ]
