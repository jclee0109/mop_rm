from .models import SubjectInfo


for i in range(300):

    name=sub[i]
    code= code[i]
    professor=prof[i]
    day1=day[i][0], day2=day[i][1], day3=day[i][2], day4=day[i][3]
    start_h1=time[i][0][0][0], start_m1=time[i][0][0][1], fin_h1=time[i][0][1][0], fin_m1=time[i][0][1][1]
    start_h2=time[i][1][0][0], start_m2=time[i][1][0][1], fin_h2=time[i][1][1][0], fin_m2=time[i][1][1][1]
    start_h3=time[i][2][0][0], start_m3=time[i][2][0][1], fin_h3=time[i][2][1][0], fin_m3=time[i][2][1][1]
    start_h4=time[i][3][0][0], start_m4=time[i][3][0][1], fin_h4=time[i][3][1][0], fin_m4=time[i][3][1][1]
    sub.save()
    code.save()
    day.save()
    prof.save()
    time.save()