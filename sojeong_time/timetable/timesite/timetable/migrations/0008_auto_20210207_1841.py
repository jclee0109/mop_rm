# Generated by Django 3.1.3 on 2021-02-07 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0007_userchoice'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userchoice',
            old_name='subject_selected1',
            new_name='subject_selected',
        ),
        migrations.AddField(
            model_name='subjectinfo',
            name='index',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
    ]
