# Generated by Django 3.1.3 on 2021-02-08 08:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0006_auto_20210208_1728'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subject_add',
            old_name='subject',
            new_name='subject_add',
        ),
    ]