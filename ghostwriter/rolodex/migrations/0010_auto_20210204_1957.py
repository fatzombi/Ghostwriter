# Generated by Django 3.0.10 on 2021-02-04 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rolodex', '0009_projecttarget'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projecttarget',
            name='ip_address',
            field=models.GenericIPAddressField(blank=True, help_text="Enter the target's IP address", null=True, verbose_name='IP Address'),
        ),
    ]