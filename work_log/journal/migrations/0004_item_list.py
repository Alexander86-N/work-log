# Generated by Django 4.1.3 on 2022-12-09 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("journal", "0003_list"),
    ]

    operations = [
        migrations.AddField(
            model_name="item",
            name="list",
            field=models.TextField(default=""),
        ),
    ]