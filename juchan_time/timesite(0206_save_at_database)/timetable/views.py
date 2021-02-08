from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from .models import SubjectInfo,Subject_add
from timetable.models import SubjectInfo
import re
import pandas as pd
import numpy
from django.db.models import Q
from django.contrib.auth.models import User

# ---------------------------------------------------------------------------- #

def index(request):
    return render(request, 'timetable/color.html')

def main(request):
    """
        강의 목록 출력
        """
    page = request.GET.get('page', '1')  # 페이지
    kw = request.GET.get('kw', '')  # 검색어
    subject_list = SubjectInfo.objects.order_by('name')
    if kw:
        subject_list = subject_list.filter(
            Q(name__icontains=kw) |
            Q(professor1__icontains=kw)
        )

    paginator = Paginator(subject_list, 10)
    page_obj = paginator.get_page(page)

    context = {'subject_list': page_obj, 'page': page, 'kw': kw}
    return render(request, 'timetable/main.html', context)

def mytable(request, user_id):
    page = request.GET.get('page', '1')  # 페이지
    kw = request.GET.get('kw', '')  # 검색어
    subject_list = SubjectInfo.objects.order_by('id')
    subject_add_list = Subject_add.objects.filter(user_id=request.user.id).values('subject_add_id').distinct().order_by('subject_add_id')
    subject_selected_list = []
    for i in range(len(subject_add_list)):
        subject_selected_list.append(SubjectInfo.objects.get(id=subject_add_list[i].get('subject_add_id')))
        #subject_add_list는 list형태인 것 같고, i는 정수형태로 받았어.
        #처음에 for i in subject_add_list 로 했었는데 i를 딕셔너리 형태로 받더라... 그래서 정수형으로 바꿔주고
        #이제 subject_add_list[i]가 딕셔너리 형태로 되어있을 건데 --> { 'subject_add_id' = 188 } 이런 식으로
        #나는 188의 값만 필요하니깐 subject_add_id를 키값으로 하는 값을 출력했어. 그게 get함수야
        #이렇게 subject_selected_list를 만들었고, 결국 얘네를 main.html에 집어넣으면서 끝나

    if kw:
        subject_list = subject_list.filter(
            Q(name__icontains=kw) |
            Q(professor1__icontains=kw)|
            Q(id__icontains=kw)|
            Q(code__icontains=kw)
        )

    paginator = Paginator(subject_list, 10)
    page_obj = paginator.get_page(page)

    context = {'subject_list': page_obj, 'page': page, 'kw': kw, 'subject_selected_list': subject_selected_list}
    return render(request, 'timetable/main.html', context)

def choice_subject(request, subject_id, user_id):
    subject = get_object_or_404(SubjectInfo, pk=subject_id)
    subject.choice.add(request.user)
    return redirect('timetable:mytable', user_id=request.user.id)

def add(request, subject_id):
    """
    과목 추가
    """
    if request.method == 'GET':
        tmp = Subject_add()

        tmp_subject = SubjectInfo.objects.get(id=subject_id)
        tmp_add = SubjectInfo.objects.get(id=subject_id)
        tmp_add.added = True
        tmp.subject_add = tmp_subject
        tmp.user = request.user
        tmp.save()
        return redirect('timetable:mytable', user_id=request.user.id)

def delete(request, subject_id):
    """
    과목 삭제
    """
    if request.method == 'GET':
        tmp_delete = SubjectInfo.objects.get(id=subject_id)
        tmp_delete.added = False
        temp = Subject_add.objects.filter(subject_add_id=subject_id, user_id = request.user.id)
        temp.delete()
    return redirect('timetable:mytable', user_id=request.user.id)


def data_save(request):
    # 엑셀파일 받기
    Location = 'C:/Users/이주찬/Desktop/rmathing/mop_rm'
    # 이거 바꿔줄 필요 있음
    File = 'Excel_Timetable.xls'

    data_pd = pd.read_excel('{}/{}'.format(Location, File),
                            header=None, index_col=None, names=None)
    data_np = pd.DataFrame.to_numpy(data_pd)
    time = []

    # 시간정보 읽어오기
    for i in range(1, len(data_pd)):
        time.append(re.findall("\d+", str(data_pd[11][i])))
    for i in range(len(time)):
        time[i] = numpy.array(time[i]).reshape(len(time[i]) // 4, 2, 2)

    # 요일정보 읽어오기
    day = []
    for i in range(1, len(data_pd)):
        day.append(re.compile("[가-힣]+").findall(str(data_pd[11][i])))

    # 교수님정보 읽어오기
    prof = []
    for i in range(1, len(data_pd)):
        prof.append(re.compile("[가-힣]+").findall(str(data_pd[8][i])))

    # 과목명 읽어오기
    sub = []
    for i in range(1, len(data_pd)):
        sub.append(data_pd[5][i])

    # 과목코드 읽어오기
    code = []
    for i in range(1, len(data_pd)):
        code.append(data_pd[4][i])

    for i in range(len(data_pd) - 1):
        subject = SubjectInfo(name=sub[i], code=code[i])
        if (len(prof[i]) == 1):
            subject.professor1 = prof[i][0]
        elif (len(prof[i]) == 2):
            subject.professor1 = prof[i][0]
            subject.professor2 = prof[i][1]

        if (len(day[i]) == 1):
            subject.day1 = day[i][0]
            subject.start_time1 = time[i][0][0][0] + ":" + time[i][0][0][1]
            subject.finish_time1 = time[i][0][1][0] + ":" + time[i][0][1][1]
            subject.start_h1 = int(time[i][0][0][0])
            subject.start_m1 = int(time[i][0][0][1])

            subject.fin_h1 = int(time[i][0][1][0])
            subject.fin_m1 = int(time[i][0][1][1])
            subject.count = 1

        elif (len(day[i]) == 2):
            subject.day1 = day[i][0]
            subject.day2 = day[i][1]
            subject.start_time1 = time[i][0][0][0] + ":" + time[i][0][0][1]
            subject.start_time2 = time[i][1][0][0] + ":" + time[i][1][0][1]
            subject.finish_time1 = time[i][0][1][0] + ":" + time[i][0][1][1]
            subject.finish_time2 = time[i][1][1][0] + ":" + time[i][1][1][1]
            subject.start_h1 = int(time[i][0][0][0])
            subject.start_m1 = int(time[i][0][0][1])
            subject.fin_h1 = int(time[i][0][1][0])
            subject.fin_m1 = int(time[i][0][1][1])
            subject.start_h2 = int(time[i][1][0][0])
            subject.start_m2 = int(time[i][1][0][1])
            subject.fin_h2 = int(time[i][1][1][0])
            subject.fin_m2 = int(time[i][1][1][1])
            subject.count = 2

        elif (len(day[i]) == 3):
            subject.day1 = day[i][0]
            subject.day2 = day[i][1]
            subject.day3 = day[i][2]
            subject.start_time1 = time[i][0][0][0] + ":" + time[i][0][0][1]
            subject.start_time2 = time[i][1][0][0] + ":" + time[i][1][0][1]
            subject.start_time3 = time[i][2][0][0] + ":" + time[i][2][0][1]
            subject.finish_time1 = time[i][0][1][0] + ":" + time[i][0][1][1]
            subject.finish_time2 = time[i][1][1][0] + ":" + time[i][1][1][1]
            subject.finish_time3 = time[i][2][1][0] + ":" + time[i][2][1][1]
            subject.start_h1 = int(time[i][0][0][0])
            subject.start_m1 = int(time[i][0][0][1])
            subject.fin_h1 = int(time[i][0][1][0])
            subject.fin_m1 = int(time[i][0][1][1])
            subject.start_h2 = int(time[i][1][0][0])
            subject.start_m2 = int(time[i][1][0][1])
            subject.fin_h2 = int(time[i][1][1][0])
            subject.fin_m2 = int(time[i][1][1][1])
            subject.start_h3 = int(time[i][2][0][0])
            subject.start_m3 = int(time[i][2][0][1])
            subject.fin_h3 = int(time[i][2][1][0])
            subject.fin_m3 = int(time[i][2][1][1])
            subject.count = 3

        elif (len(day[i]) == 4):
            subject.day1 = day[i][0]
            subject.day2 = day[i][1]
            subject.day3 = day[i][2]
            subject.day4 = day[i][3]
            subject.start_time1 = time[i][0][0][0] + ":" + time[i][0][0][1]
            subject.start_time2 = time[i][1][0][0] + ":" + time[i][1][0][1]
            subject.start_time3 = time[i][2][0][0] + ":" + time[i][2][0][1]
            subject.start_time4 = time[i][3][0][0] + ":" + time[i][3][0][1]
            subject.finish_time1 = time[i][0][1][0] + ":" + time[i][0][1][1]
            subject.finish_time2 = time[i][1][1][0] + ":" + time[i][1][1][1]
            subject.finish_time3 = time[i][2][1][0] + ":" + time[i][2][1][1]
            subject.finish_time4 = time[i][3][1][0] + ":" + time[i][3][1][1]
            subject.start_h1 = int(time[i][0][0][0])
            subject.start_m1 = int(time[i][0][0][1])
            subject.fin_h1 = int(time[i][0][1][0])
            subject.fin_m1 = int(time[i][0][1][1])
            subject.start_h2 = int(time[i][1][0][0])
            subject.start_m2 = int(time[i][1][0][1])
            subject.fin_h2 = int(time[i][1][1][0])
            subject.fin_m2 = int(time[i][1][1][1])
            subject.start_h3 = int(time[i][2][0][0])
            subject.start_m3 = int(time[i][2][0][1])
            subject.fin_h3 = int(time[i][2][1][0])
            subject.fin_m3 = int(time[i][2][1][1])
            subject.start_h4 = int(time[i][3][0][0])
            subject.start_m4 = int(time[i][3][0][1])
            subject.fin_h4 = int(time[i][3][1][0])
            subject.fin_m4 = int(time[i][3][1][1])
            subject.count = 4
        subject.save()

    return render(request, 'timetable/main.html')

