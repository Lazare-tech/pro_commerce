# Generated by Django 4.2.13 on 2024-09-08 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("compte", "0007_remove_user_otp_remove_user_otp_expiry"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="otp",
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
        migrations.AddField(
            model_name="user",
            name="otp_expiry",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
