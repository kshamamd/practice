# Generated by Django 3.1.4 on 2021-01-23 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('color', '0012_creatordesign_design_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='creatordesign',
            name='design_name',
            field=models.CharField(default='art', max_length=50),
        ),
    ]