# Generated by Django 4.1.7 on 2023-06-04 08:07

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("network", "0015_alter_user_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="id",
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
    ]
