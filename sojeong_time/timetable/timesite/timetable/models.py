from django.db import models


# Create your models here.
class SubjectInfo(models.Model):
    name=models.CharField(max_length=100, default='')
    code=models.CharField(max_length=100, default='')

    professor1=models.CharField(max_length=100, default='')
    professor2=models.CharField(max_length=100, blank=True, default='')

    day1=models.CharField(max_length=1, default='')
    day2=models.CharField(max_length=1, blank=True, default='')
    day3=models.CharField(max_length=1, blank=True, default='')
    day4=models.CharField(max_length=1, blank=True, default='')

    start_time1=models.CharField(max_length=100, default='')
    start_time2=models.CharField(max_length=100, blank=True, default='')
    start_time3=models.CharField(max_length=100, blank=True, default='')
    start_time4=models.CharField(max_length=100, blank=True, default='')
    finish_time1=models.CharField(max_length=100, blank=True, default='')
    finish_time2=models.CharField(max_length=100, blank=True, default='')
    finish_time3=models.CharField(max_length=100, blank=True, default='')
    finish_time4=models.CharField(max_length=100, blank=True, default='')

    start_h1=models.PositiveSmallIntegerField(blank=True, null=True)
    start_m1=models.PositiveSmallIntegerField(blank=True, null=True)
    fin_h1=models.PositiveSmallIntegerField(blank=True, null=True)
    fin_m1=models.PositiveSmallIntegerField(blank=True, null=True)

    start_h2=models.PositiveSmallIntegerField(blank=True, null=True)
    start_m2=models.PositiveSmallIntegerField(blank=True, null=True)
    fin_h2=models.PositiveSmallIntegerField(blank=True, null=True)
    fin_m2=models.PositiveSmallIntegerField(blank=True, null=True)

    start_m3=models.PositiveSmallIntegerField(blank=True, null=True)
    start_h3=models.PositiveSmallIntegerField(blank=True, null=True)
    fin_h3=models.PositiveSmallIntegerField(blank=True, null=True)
    fin_m3=models.PositiveSmallIntegerField(blank=True, null=True)

    start_h4=models.PositiveSmallIntegerField(blank=True, null=True)
    start_m4=models.PositiveSmallIntegerField(blank=True, null=True)
    fin_h4=models.PositiveSmallIntegerField(blank=True, null=True)
    fin_m4=models.PositiveSmallIntegerField(blank=True, null=True)

    def __str__(self):
        return self.name