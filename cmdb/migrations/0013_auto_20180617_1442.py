# Generated by Django 2.0.4 on 2018-06-17 06:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0012_tag_creator'),
    ]

    operations = [
        migrations.RenameField(
            model_name='users',
            old_name='publishers_name',
            new_name='publishers_ISBN',
        ),
    ]
