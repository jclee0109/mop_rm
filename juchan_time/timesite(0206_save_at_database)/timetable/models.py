from django.db import models

# Create your models here.

class SubjectInfo(models.Model):

    name=models.CharField(max_length=100, blank=True, null=True)
    code=models.CharField(max_length=100, blank=True, null=True)
    professor1=models.CharField(max_length=100, blank=True, null=True)
    professor2=models.CharField(max_length=100, blank=True, null=True)

    day1=models.CharField(max_length=1, blank=True, null=True)
    day2=models.CharField(max_length=1, blank=True, null=True)
    day3=models.CharField(max_length=1, blank=True, null=True)
    day4=models.CharField(max_length=1, blank=True, null=True)

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

    start_time1=models.CharField(max_length=100, blank=True, null=True)
    start_time2=models.CharField(max_length=100, blank=True, null=True)
    start_time3=models.CharField(max_length=100, blank=True, null=True)
    start_time4=models.CharField(max_length=100, blank=True, null=True)
    finish_time1=models.CharField(max_length=100, blank=True, null=True)
    finish_time2=models.CharField(max_length=100, blank=True, null=True)
    finish_time3=models.CharField(max_length=100, blank=True, null=True)
    finish_time4=models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name