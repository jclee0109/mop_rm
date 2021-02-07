# Generated by Django 3.1.3 on 2021-02-07 14:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0008_auto_20210207_1841'),
    ]

    operations = [
        migrations.AddField(
            model_name='subjectinfo',
            name='count',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='userchoice',
            name='subject_selected',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='timetable.subjectinfo'),
        ),
    ]