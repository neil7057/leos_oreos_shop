# Generated by Django 5.1.6 on 2025-02-20 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_alter_userprofile_default_country'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='default_full_name',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
