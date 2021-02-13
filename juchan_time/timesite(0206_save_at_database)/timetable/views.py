from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from .models import SubjectInfo, Subject_add
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from django.shortcuts import render, get_object_or_404
from rest_framework import generics
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView
import re
import pandas as pd
import numpy
from django.db.models import Q
from django.contrib.auth.models import User
from django.http import HttpResponse


# ---------------------------------------------------------------------------- #

def index(request):
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
    return render(request, 'timetable/index.html', context)

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

# @login_required(login_url='common:login')
# def mytable(request, user_id):
#     page = request.GET.get('page', '1')  # 페이지
#
#     drop1 = request.GET.get('drop1', '') #요일
#     subject_list = SubjectInfo.objects.order_by('id')
#     subject_add_list = Subject_add.objects.filter(user_id=request.user.id).values('subject_add_id').distinct().order_by('subject_add_id')
#     subject_selected_list = []
#     sum = 0
#     for i in range(len(subject_add_list)):
#         subject_selected_list.append(SubjectInfo.objects.get(id=subject_add_list[i].get('subject_add_id')))
#         #subject_add_list는 list형태인 것 같고, i는 정수형태로 받았어.
#         #처음에 for i in subject_add_list 로 했었는데 i를 딕셔너리 형태로 받더라... 그래서 정수형으로 바꿔주고
#         #이제 subject_add_list[i]가 딕셔너리 형태로 되어있을 건데 --> { 'subject_add_id' = 188 } 이런 식으로
#         #나는 188의 값만 필요하니깐 subject_add_id를 키값으로 하는 값을 출력했어. 그게 get함수야
#         #이렇게 subject_selected_list를 만들었고, 결국 얘네를 main.html에 집어넣으면서 끝나
#
#     for i in range(len(subject_selected_list)):
#         sum += subject_selected_list[i].credit
#
#     if kw:
#         subject_list = subject_list.filter(
#             Q(name__icontains=kw) |
#             Q(professor1__icontains=kw)|
#             Q(id__icontains=kw)|
#             Q(code__icontains=kw)
#         )
#
#     paginator = Paginator(subject_list, 10)
#     page_obj = paginator.get_page(page)
#
#
#     context = {'subject_list': page_obj, 'page': page, 'kw': kw, 'subject_selected_list': subject_selected_list,
#                'sum':sum, 'drop1':drop1}
#     return render(request, 'timetable/main.html', context)


def is_valid_queryparam(param):
    return param != '' and param is not None

@login_required(login_url='common:login')
def mytable(request, user_id):
    page = request.GET.get('page', '1')  # 페이지
    kw = request.GET.get('kw', '')  # 검색어
    name = request.GET.get('name') # 과목이름
    professor = request.GET.get('professor')
    id = request.GET.get('id') # 과목ID
    code = request.GET.get('code') # 과목코드
    day = request.GET.get('day') # 요일
    time = request.GET.get('time') # 시간
    department = request.GET.get('department') # 부서
    subject_list = SubjectInfo.objects.order_by('id')
    subject_add_list = Subject_add.objects.filter(user_id=request.user.id).values('subject_add_id').distinct().order_by('subject_add_id')
    subject_selected_list = []
    sum = 0
    for i in range(len(subject_add_list)):
        subject_selected_list.append(SubjectInfo.objects.get(id=subject_add_list[i].get('subject_add_id')))
        #subject_add_list는 list형태인 것 같고, i는 정수형태로 받았어.
        #처음에 for i in subject_add_list 로 했었는데 i를 딕셔너리 형태로 받더라... 그래서 정수형으로 바꿔주고
        #이제 subject_add_list[i]가 딕셔너리 형태로 되어있을 건데 --> { 'subject_add_id' = 188 } 이런 식으로
        #나는 188의 값만 필요하니깐 subject_add_id를 키값으로 하는 값을 출력했어. 그게 get함수야
        #이렇게 subject_selected_list를 만들었고, 결국 얘네를 main.html에 집어넣으면서 끝나

    for i in range(len(subject_selected_list)):
        sum += subject_selected_list[i].credit

    qs = SubjectInfo.objects.all()
    if is_valid_queryparam(name):
        qs = qs.filter(name__icontains=name)
    if is_valid_queryparam(professor):
        qs = qs.filter(
            Q(professor1__icontains = professor)|
            Q(professor2__icontains = professor)
        )
    if is_valid_queryparam(code):
        qs = qs.filter(code=code)
    if is_valid_queryparam(id):
        qs = qs.filter(id=id)
    if is_valid_queryparam(day):
        if is_valid_queryparam(time):
            qs = qs.filter(
                Q(day1 = day, start_time1 = time)|
                Q(day2 = day, start_time2 = time)|
                Q(day3 = day, start_time3 = time)|
                Q(day4 = day, start_time4 = time)
            )
        else:
            qs = qs.filter(
                Q(day1=day) |
                Q(day2=day) |
                Q(day3=day) |
                Q(day4=day)
            )
    elif is_valid_queryparam(time):
        qs = qs.filter(
            Q(start_time1 = time)|
            Q(start_time2 = time)|
            Q(start_time3 = time)|
            Q(start_time4 = time)
        )
    if is_valid_queryparam(department):
        qs = qs.filter(department=department)

    if kw:
        subject_list = subject_list.filter(
            Q(name__icontains=kw) |
            Q(professor1__icontains=kw)|
            Q(id__icontains=kw)|
            Q(code__icontains=kw)
        )

    paginator = Paginator(qs, 10)
    page_obj = paginator.get_page(page)


    context = {'subject_list': page_obj, 'page': page, 'kw': kw, 'subject_selected_list': subject_selected_list,
               'sum':sum}
    return render(request, 'timetable/main.html', context)


def add(request, subject_id):
    """
    과목 추가
    """
    if request.method == 'GET':
        tmp_subject = SubjectInfo.objects.get(id=subject_id)
        subject_add_list = Subject_add.objects.filter(user_id=request.user.id).values('subject_add_id').distinct()
        subject_selected_list = []
        for i in range(len(subject_add_list)):
            subject_selected_list.append(SubjectInfo.objects.get(id=subject_add_list[i].get('subject_add_id')))
        overlap = False
        is_same_subject = False
        for subject in subject_selected_list:
            if tmp_subject.id == subject.id:
                messages.error(request, '이미 같은 강의가 장바구니에 있습니다.', ['선택한 강의 -> ID:', tmp_subject.id, 'Name:', tmp_subject.name])
                return redirect('timetable:mytable', user_id=request.user.id)
            else:
                continue
        #1일짜리 강의 겹치는지 체크
        if tmp_subject.count == 1:
            for subject in subject_selected_list:
                if subject.count == 1:
                    if tmp_subject.day1 == subject.day1:
                        if tmp_subject.start_h1 * 60 + tmp_subject.start_m1 >= subject.fin_h1 * 60 + subject.fin_m1 or tmp_subject.fin_h1 * 60 + tmp_subject.fin_m1 <= subject.start_h1 * 60 + subject.start_m1:
                            pass
                        else:
                            overlap = True
                            break

                elif subject.count == 2:
                    if tmp_subject.day1 == subject.day1:
                        if  tmp_subject.start_h1 * 60 + tmp_subject.start_m1 >= subject.fin_h1 * 60 + subject.fin_m1 or tmp_subject.fin_h1 * 60 + tmp_subject.fin_m1 <= subject.start_h1 * 60 + subject.start_m1:
                            pass
                        else:
                            overlap = True
                            break
                    if tmp_subject.day1 == subject.day2:
                        if tmp_subject.start_h1 * 60 + tmp_subject.start_m1 >= subject.fin_h2 * 60 + subject.fin_m2 or tmp_subject.fin_h1 * 60 + tmp_subject.fin_m1 <= subject.start_h2 * 60 + subject.start_m2:
                            pass
                        else:
                            overlap = True
                            break

                elif subject.count == 3:
                    if tmp_subject.day1 == subject.day1:
                        if tmp_subject.start_h1 * 60 + tmp_subject.start_m1 >= subject.fin_h1 * 60 + subject.fin_m1 or tmp_subject.fin_h1 * 60 + tmp_subject.fin_m1 <= subject.start_h1 * 60 + subject.start_m1:
                            pass
                        else:
                            overlap = True
                            break
                    if tmp_subject.day1 == subject.day2:
                        if tmp_subject.start_h1 * 60 + tmp_subject.start_m1 >= subject.fin_h2 * 60 + subject.fin_m2 or tmp_subject.fin_h1 * 60 + tmp_subject.fin_m1 <= subject.start_h2 * 60 + subject.start_m2:
                            pass
                        else:
                            overlap = True
                            break
                    if tmp_subject.day1 == subject.day3:
                        if  tmp_subject.start_h1 * 60 + tmp_subject.start_m1 >= subject.fin_h3 * 60 + subject.fin_m3 or tmp_subject.fin_h1 * 60 + tmp_subject.fin_m1 <= subject.start_h3 * 60 + subject.start_m3:
                            pass
                        else:
                            overlap = True
                            break
                elif subject.count == 4:
                    if tmp_subject.day1 == subject.day1:
                        if  tmp_subject.start_h1 * 60 + tmp_subject.start_m1 >= subject.fin_h1 * 60 + subject.fin_m1 or tmp_subject.fin_h1 * 60 + tmp_subject.fin_m1 <= subject.start_h1 * 60 + subject.start_m1:
                            pass
                        else:
                            overlap = True
                            break
                    if tmp_subject.day1 == subject.day2:
                        if  tmp_subject.start_h1 * 60 + tmp_subject.start_m1 >= subject.fin_h2 * 60 + subject.fin_m2 or tmp_subject.fin_h1 * 60 + tmp_subject.fin_m1 <= subject.start_h2 * 60 + subject.start_m2:
                            pass
                        else:
                            overlap = True
                            break
                    if tmp_subject.day1 == subject.day3:
                        if  tmp_subject.start_h1 * 60 + tmp_subject.start_m1 >= subject.fin_h3 * 60 + subject.fin_m3 or tmp_subject.fin_h1 * 60 + tmp_subject.fin_m1 <= subject.start_h3 * 60 + subject.start_m3:
                            pass
                        else:
                            overlap = True
                            break
                    if tmp_subject.day1 == subject.day4:
                        if  tmp_subject.start_h1 * 60 + tmp_subject.start_m1 >= subject.fin_h4 * 60 + subject.fin_m4 or tmp_subject.fin_h1 * 60 + tmp_subject.fin_m1 <= subject.start_h4 * 60 + subject.start_m4:
                            pass
                        else:
                            overlap = True
                            break
        # 2일짜리 강의 겹치는지 check
        elif tmp_subject.count == 2:
            for subject in subject_selected_list:
                if subject.count == 1:
                    if tmp_subject.day1 == subject.day1:
                        if tmp_subject.start_h1 * 60 + tmp_subject.start_m1 >= subject.fin_h1 * 60 + subject.fin_m1 or tmp_subject.fin_h1 * 60 + tmp_subject.fin_m1 <= subject.start_h1 * 60 + subject.start_m1:
                            pass
                        else:
                            overlap = True
                            break
                    if tmp_subject.day2 == subject.day1:
                        if tmp_subject.start_h2 * 60 + tmp_subject.start_m2 >= subject.fin_h1 * 60 + subject.fin_m1 or tmp_subject.fin_h2 * 60 + tmp_subject.fin_m2 <= subject.start_h1 * 60 + subject.start_m1:
                            pass
                        else:
                            overlap = True
                            break

                elif subject.count == 2:
                    if tmp_subject.day1 == subject.day1:
                        if  tmp_subject.start_h1 * 60 + tmp_subject.start_m1 >= subject.fin_h1 * 60 + subject.fin_m1 or tmp_subject.fin_h1 * 60 + tmp_subject.fin_m1 <= subject.start_h1 * 60 + subject.start_m1:
                            pass
                        else:
                            overlap = True
                            break
                    if tmp_subject.day1 == subject.day2:
                        if  tmp_subject.start_h1 * 60 + tmp_subject.start_m1 >= subject.fin_h2 * 60 + subject.fin_m2 or tmp_subject.fin_h1 * 60 + tmp_subject.fin_m1 <= subject.start_h2 * 60 + subject.start_m2:
                            pass
                        else:
                            overlap = True
                            break
                    if tmp_subject.day2 == subject.day1:
                        if  tmp_subject.start_h2 * 60 + tmp_subject.start_m2 >= subject.fin_h1 * 60 + subject.fin_m1 or tmp_subject.fin_h2 * 60 + tmp_subject.fin_m2 <= subject.start_h1 * 60 + subject.start_m1:
                            pass
                        else:
                            overlap = True
                            break
                    if tmp_subject.day2 == subject.day2:
                        if  tmp_subject.start_h2 * 60 + tmp_subject.start_m2 >= subject.fin_h2 * 60 + subject.fin_m2 or tmp_subject.fin_h2 * 60 + tmp_subject.fin_m2 <= subject.start_h2 * 60 + subject.start_m2:
                            pass
                        else:
                            overlap = True
                            break
                elif subject.count == 3:
                    if tmp_subject.day1 == subject.day1:
                        if  tmp_subject.start_h1 * 60 + tmp_subject.start_m1 >= subject.fin_h1 * 60 + subject.fin_m1 or tmp_subject.fin_h1 * 60 + tmp_subject.fin_m1 <= subject.start_h1 * 60 + subject.start_m1:
                            pass
                        else:
                            overlap = True
                            break
                    if tmp_subject.day1 == subject.day2:
                        if  tmp_subject.start_h1 * 60 + tmp_subject.start_m1 >= subject.fin_h2 * 60 + subject.fin_m2 or tmp_subject.fin_h1 * 60 + tmp_subject.fin_m1 <= subject.start_h2 * 60 + subject.start_m2:
                            pass
                        else:
                            overlap = True
                            break
                    if tmp_subject.day1 == subject.day3:
                        if  tmp_subject.start_h1 * 60 + tmp_subject.start_m1 >= subject.fin_h3 * 60 + subject.fin_m3 or tmp_subject.fin_h1 * 60 + tmp_subject.fin_m1 <= subject.start_h3 * 60 + subject.start_m3:
                            pass
                        else:
                            overlap = True
                            break
                    if tmp_subject.day2 == subject.day1:
                        if  tmp_subject.start_h2 * 60 + tmp_subject.start_m2 >= subject.fin_h1 * 60 + subject.fin_m1 or tmp_subject.fin_h2 * 60 + tmp_subject.fin_m2 <= subject.start_h1 * 60 + subject.start_m1:
                            pass
                        else:
                            overlap = True
                            break
                    if tmp_subject.day2 == subject.day2:
                        if  tmp_subject.start_h2 * 60 + tmp_subject.start_m2 >= subject.fin_h2 * 60 + subject.fin_m2 or tmp_subject.fin_h2 * 60 + tmp_subject.fin_m2 <= subject.start_h2 * 60 + subject.start_m2:
                            pass
                        else:
                            overlap = True
                            break
                    if tmp_subject.day2 == subject.day3:
                        if  tmp_subject.start_h2 * 60 + tmp_subject.start_m2 >= subject.fin_h3 * 60 + subject.fin_m3 or tmp_subject.fin_h2 * 60 + tmp_subject.fin_m2 <= subject.start_h3 * 60 + subject.start_m3:
                            pass
                        else:
                            overlap = True
                            break
                elif subject.count == 4:
                    if tmp_subject.day1 == subject.day1:
                        if  tmp_subject.start_h1 * 60 + tmp_subject.start_m1 >= subject.fin_h1 * 60 + subject.fin_m1 or tmp_subject.fin_h1 * 60 + tmp_subject.fin_m1 <= subject.start_h1 * 60 + subject.start_m1:
                            pass
                        else:
                            overlap = True
                            break
                    if tmp_subject.day1 == subject.day2:
                        if  tmp_subject.start_h1 * 60 + tmp_subject.start_m1 >= subject.fin_h2 * 60 + subject.fin_m2 or tmp_subject.fin_h1 * 60 + tmp_subject.fin_m1 <= subject.start_h2 * 60 + subject.start_m2:
                            pass
                        else:
                            overlap = True
                            break
                    if tmp_subject.day1 == subject.day3:
                        if  tmp_subject.start_h1 * 60 + tmp_subject.start_m1 >= subject.fin_h3 * 60 + subject.fin_m3 or tmp_subject.fin_h1 * 60 + tmp_subject.fin_m1 <= subject.start_h3 * 60 + subject.start_m3:
                            pass
                        else:
                            overlap = True
                            break
                    if tmp_subject.day1 == subject.day4:
                        if  tmp_subject.start_h1 * 60 + tmp_subject.start_m1 >= subject.fin_h4 * 60 + subject.fin_m4 or tmp_subject.fin_h1 * 60 + tmp_subject.fin_m1 <= subject.start_h4 * 60 + subject.start_m4:
                            pass
                        else:
                            overlap = True
                            break
                    if tmp_subject.day2 == subject.day1:
                        if  tmp_subject.start_h2 * 60 + tmp_subject.start_m2 >= subject.fin_h1 * 60 + subject.fin_m1 or tmp_subject.fin_h2 * 60 + tmp_subject.fin_m2 <= subject.start_h1 * 60 + subject.start_m1:
                            pass
                        else:
                            overlap = True
                            break
                    if tmp_subject.day2 == subject.day2:
                        if  tmp_subject.start_h2 * 60 + tmp_subject.start_m2 >= subject.fin_h2 * 60 + subject.fin_m2 or tmp_subject.fin_h2 * 60 + tmp_subject.fin_m2 <= subject.start_h2 * 60 + subject.start_m2:
                            pass
                        else:
                            overlap = True
                            break
                    if tmp_subject.day2 == subject.day3:
                        if  tmp_subject.start_h2 * 60 + tmp_subject.start_m2 >= subject.fin_h3 * 60 + subject.fin_m3 or tmp_subject.fin_h2 * 60 + tmp_subject.fin_m2 <= subject.start_h3 * 60 + subject.start_m3:
                            pass
                        else:
                            overlap = True
                            break
                    if tmp_subject.day2 == subject.day4:
                        if  tmp_subject.start_h2 * 60 + tmp_subject.start_m2 >= subject.fin_h4 * 60 + subject.fin_m4 or tmp_subject.fin_h2 * 60 + tmp_subject.fin_m2 <= subject.start_h4 * 60 + subject.start_m4:
                            pass
                        else:
                            overlap = True
                            break
        # 3일짜리 강의가 겹치는지 체크
        elif tmp_subject.count == 3:
            for subject in subject_selected_list:
                if subject.count == 1:
                    if tmp_subject.day1 == subject.day1:
                        if tmp_subject.start_h1 * 60 + tmp_subject.start_m1 >= subject.fin_h1 * 60 + subject.fin_m1 or tmp_subject.fin_h1 * 60 + tmp_subject.fin_m1 <= subject.start_h1 * 60 + subject.start_m1:
                            pass
                        else:
                            overlap = True
                            break
                    if tmp_subject.day2 == subject.day1:
                        if tmp_subject.start_h2 * 60 + tmp_subject.start_m2 >= subject.fin_h1 * 60 + subject.fin_m1 or tmp_subject.fin_h2 * 60 + tmp_subject.fin_m2 <= subject.start_h1 * 60 + subject.start_m1:
                            pass
                        else:
                            overlap = True
                            break
                    if tmp_subject.day3 == subject.day1:
                        if tmp_subject.start_h3 * 60 + tmp_subject.start_m3 >= subject.fin_h1 * 60 + subject.fin_m1 or tmp_subject.fin_h3 * 60 + tmp_subject.fin_m3 <= subject.start_h1 * 60 + subject.start_m1:
                            pass
                        else:
                            overlap = True
                            break

                elif subject.count == 2:
                    if tmp_subject.day1 == subject.day1:
                        if tmp_subject.start_h1 * 60 + tmp_subject.start_m1 >= subject.fin_h1 * 60 + subject.fin_m1 or tmp_subject.fin_h1 * 60 + tmp_subject.fin_m1 <= subject.start_h1 * 60 + subject.start_m1:
                            pass
                        else:
                            overlap = True
                            break
                    if tmp_subject.day1 == subject.day2:
                        if tmp_subject.start_h1 * 60 + tmp_subject.start_m1 >= subject.fin_h2 * 60 + subject.fin_m2 or tmp_subject.fin_h1 * 60 + tmp_subject.fin_m1 <= subject.start_h2 * 60 + subject.start_m2:
                            pass
                        else:
                            overlap = True
                            break
                    if tmp_subject.day2 == subject.day1:
                        if tmp_subject.start_h2 * 60 + tmp_subject.start_m2 >= subject.fin_h1 * 60 + subject.fin_m1 or tmp_subject.fin_h2 * 60 + tmp_subject.fin_m2 <= subject.start_h1 * 60 + subject.start_m1:
                            pass
                        else:
                            overlap = True
                            break
                    if tmp_subject.day2 == subject.day2:
                        if tmp_subject.start_h2 * 60 + tmp_subject.start_m2 >= subject.fin_h2 * 60 + subject.fin_m2 or tmp_subject.fin_h2 * 60 + tmp_subject.fin_m2 <= subject.start_h2 * 60 + subject.start_m2:
                            pass
                        else:
                            overlap = True
                            break
                    if tmp_subject.day3 == subject.day1:
                        if tmp_subject.start_h3 * 60 + tmp_subject.start_m3 >= subject.fin_h1 * 60 + subject.fin_m1 or tmp_subject.fin_h3 * 60 + tmp_subject.fin_m3 <= subject.start_h1 * 60 + subject.start_m1:
                            pass
                        else:
                            overlap = True
                            break
                    if tmp_subject.day3 == subject.day2:
                        if tmp_subject.start_h3 * 60 + tmp_subject.start_m3 >= subject.fin_h2 * 60 + subject.fin_m2 or tmp_subject.fin_h3 * 60 + tmp_subject.fin_m3 <= subject.start_h2 * 60 + subject.start_m2:
                            pass
                        else:
                            overlap = True
                            break
                elif subject.count == 3:
                    if tmp_subject.day1 == subject.day1:
                        if tmp_subject.start_h1 * 60 + tmp_subject.start_m1 >= subject.fin_h1 * 60 + subject.fin_m1 or tmp_subject.fin_h1 * 60 + tmp_subject.fin_m1 <= subject.start_h1 * 60 + subject.start_m1:
                            pass
                        else:
                            overlap = True
                            break
                    if tmp_subject.day1 == subject.day2:
                        if tmp_subject.start_h1 * 60 + tmp_subject.start_m1 >= subject.fin_h2 * 60 + subject.fin_m2 or tmp_subject.fin_h1 * 60 + tmp_subject.fin_m1 <= subject.start_h2 * 60 + subject.start_m2:
                            pass
                        else:
                            overlap = True
                            break
                    if tmp_subject.day1 == subject.day3:
                        if tmp_subject.start_h1 * 60 + tmp_subject.start_m1 >= subject.fin_h3 * 60 + subject.fin_m3 or tmp_subject.fin_h1 * 60 + tmp_subject.fin_m1 <= subject.start_h3 * 60 + subject.start_m3:
                            pass
                        else:
                            overlap = True
                            break
                    if tmp_subject.day2 == subject.day1:
                        if tmp_subject.start_h2 * 60 + tmp_subject.start_m2 >= subject.fin_h1 * 60 + subject.fin_m1 or tmp_subject.fin_h2 * 60 + tmp_subject.fin_m2 <= subject.start_h1 * 60 + subject.start_m1:
                            pass
                        else:
                            overlap = True
                            break
                    if tmp_subject.day2 == subject.day2:
                        if tmp_subject.start_h2 * 60 + tmp_subject.start_m2 >= subject.fin_h2 * 60 + subject.fin_m2 or tmp_subject.fin_h2 * 60 + tmp_subject.fin_m2 <= subject.start_h2 * 60 + subject.start_m2:
                            pass
                        else:
                            overlap = True
                            break
                    if tmp_subject.day2 == subject.day3:
                        if tmp_subject.start_h2 * 60 + tmp_subject.start_m2 >= subject.fin_h3 * 60 + subject.fin_m3 or tmp_subject.fin_h2 * 60 + tmp_subject.fin_m2 <= subject.start_h3 * 60 + subject.start_m3:
                            pass
                        else:
                            overlap = True
                            break
                    if tmp_subject.day3 == subject.day1:
                        if tmp_subject.start_h3 * 60 + tmp_subject.start_m3 >= subject.fin_h1 * 60 + subject.fin_m1 or tmp_subject.fin_h3 * 60 + tmp_subject.fin_m3 <= subject.start_h1 * 60 + subject.start_m1:
                            pass
                        else:
                            overlap = True
                            break
                    if tmp_subject.day3 == subject.day2:
                        if tmp_subject.start_h3 * 60 + tmp_subject.start_m3 >= subject.fin_h2 * 60 + subject.fin_m2 or tmp_subject.fin_h3 * 60 + tmp_subject.fin_m3 <= subject.start_h2 * 60 + subject.start_m2:
                            pass
                        else:
                            overlap = True
                            break
                    if tmp_subject.day3 == subject.day3:
                        if tmp_subject.start_h3 * 60 + tmp_subject.start_m3 >= subject.fin_h3 * 60 + subject.fin_m3 or tmp_subject.fin_h3 * 60 + tmp_subject.fin_m3 <= subject.start_h3 * 60 + subject.start_m3:
                            pass
                        else:
                            overlap = True
                            break
                elif subject.count == 4:
                    if tmp_subject.day1 == subject.day1:
                        if tmp_subject.start_h1 * 60 + tmp_subject.start_m1 >= subject.fin_h1 * 60 + subject.fin_m1 or tmp_subject.fin_h1 * 60 + tmp_subject.fin_m1 <= subject.start_h1 * 60 + subject.start_m1:
                            pass
                        else:
                            overlap = True
                            break
                    if tmp_subject.day1 == subject.day2:
                        if tmp_subject.start_h1 * 60 + tmp_subject.start_m1 >= subject.fin_h2 * 60 + subject.fin_m2 or tmp_subject.fin_h1 * 60 + tmp_subject.fin_m1 <= subject.start_h2 * 60 + subject.start_m2:
                            pass
                        else:
                            overlap = True
                            break
                    if tmp_subject.day1 == subject.day3:
                        if tmp_subject.start_h1 * 60 + tmp_subject.start_m1 >= subject.fin_h3 * 60 + subject.fin_m3 or tmp_subject.fin_h1 * 60 + tmp_subject.fin_m1 <= subject.start_h3 * 60 + subject.start_m3:
                            pass
                        else:
                            overlap = True
                            break
                    if tmp_subject.day1 == subject.day4:
                        if tmp_subject.start_h1 * 60 + tmp_subject.start_m1 >= subject.fin_h4 * 60 + subject.fin_m4 or tmp_subject.fin_h1 * 60 + tmp_subject.fin_m1 <= subject.start_h4 * 60 + subject.start_m4:
                            pass
                        else:
                            overlap = True
                            break
                    if tmp_subject.day2 == subject.day1:
                        if tmp_subject.start_h2 * 60 + tmp_subject.start_m2 >= subject.fin_h1 * 60 + subject.fin_m1 or tmp_subject.fin_h2 * 60 + tmp_subject.fin_m2 <= subject.start_h1 * 60 + subject.start_m1:
                            pass
                        else:
                            overlap = True
                            break
                    if tmp_subject.day2 == subject.day2:
                        if tmp_subject.start_h2 * 60 + tmp_subject.start_m2 >= subject.fin_h2 * 60 + subject.fin_m2 or tmp_subject.fin_h2 * 60 + tmp_subject.fin_m2 <= subject.start_h2 * 60 + subject.start_m2:
                            pass
                        else:
                            overlap = True
                            break
                    if tmp_subject.day2 == subject.day3:
                        if tmp_subject.start_h2 * 60 + tmp_subject.start_m2 >= subject.fin_h3 * 60 + subject.fin_m3 or tmp_subject.fin_h2 * 60 + tmp_subject.fin_m2 <= subject.start_h3 * 60 + subject.start_m3:
                            pass
                        else:
                            overlap = True
                            break
                    if tmp_subject.day2 == subject.day4:
                        if tmp_subject.start_h2 * 60 + tmp_subject.start_m2 >= subject.fin_h4 * 60 + subject.fin_m4 or tmp_subject.fin_h2 * 60 + tmp_subject.fin_m2 <= subject.start_h4 * 60 + subject.start_m4:
                            pass
                        else:
                            overlap = True
                            break
                    if tmp_subject.day3 == subject.day1:
                        if tmp_subject.start_h3 * 60 + tmp_subject.start_m3 >= subject.fin_h1 * 60 + subject.fin_m1 or tmp_subject.fin_h3 * 60 + tmp_subject.fin_m3 <= subject.start_h1 * 60 + subject.start_m1:
                            pass
                        else:
                            overlap = True
                            break
                    if tmp_subject.day3 == subject.day2:
                        if tmp_subject.start_h3 * 60 + tmp_subject.start_m3 >= subject.fin_h2 * 60 + subject.fin_m2 or tmp_subject.fin_h3 * 60 + tmp_subject.fin_m3 <= subject.start_h2 * 60 + subject.start_m2:
                            pass
                        else:
                            overlap = True
                            break
                    if tmp_subject.day3 == subject.day3:
                        if tmp_subject.start_h3 * 60 + tmp_subject.start_m3 >= subject.fin_h3 * 60 + subject.fin_m3 or tmp_subject.fin_h3 * 60 + tmp_subject.fin_m3 <= subject.start_h3 * 60 + subject.start_m3:
                            pass
                        else:
                            overlap = True
                            break
                    if tmp_subject.day3 == subject.day4:
                        if tmp_subject.start_h3 * 60 + tmp_subject.start_m3 >= subject.fin_h4 * 60 + subject.fin_m4 or tmp_subject.fin_h3 * 60 + tmp_subject.fin_m3 <= subject.start_h4 * 60 + subject.start_m4:
                            pass
                        else:
                            overlap = True
                            break
        # 4일짜리 강의가 겹치는지 체크
        elif tmp_subject.count == 4:
            for subject in subject_selected_list:
                if subject.count == 1:
                    if tmp_subject.day1 == subject.day1:
                        if tmp_subject.start_h1 * 60 + tmp_subject.start_m1 >= subject.fin_h1 * 60 + subject.fin_m1 or tmp_subject.fin_h1 * 60 + tmp_subject.fin_m1 <= subject.start_h1 * 60 + subject.start_m1:
                            pass
                        else:
                            overlap = True
                            break
                    if tmp_subject.day2 == subject.day1:
                        if tmp_subject.start_h2 * 60 + tmp_subject.start_m2 >= subject.fin_h1 * 60 + subject.fin_m1 or tmp_subject.fin_h2 * 60 + tmp_subject.fin_m2 <= subject.start_h1 * 60 + subject.start_m1:
                            pass
                        else:
                            overlap = True
                            break
                    if tmp_subject.day3 == subject.day1:
                        if tmp_subject.start_h3 * 60 + tmp_subject.start_m3 >= subject.fin_h1 * 60 + subject.fin_m1 or tmp_subject.fin_h3 * 60 + tmp_subject.fin_m3 <= subject.start_h1 * 60 + subject.start_m1:
                            pass
                        else:
                            overlap = True
                            break
                    if tmp_subject.day4 == subject.day1:
                        if tmp_subject.start_h4 * 60 + tmp_subject.start_m4 >= subject.fin_h1 * 60 + subject.fin_m1 or tmp_subject.fin_h4 * 60 + tmp_subject.fin_m4 <= subject.start_h1 * 60 + subject.start_m1:
                            pass
                        else:
                            overlap = True
                            break

                elif subject.count == 2:
                    if tmp_subject.day1 == subject.day1:
                        if tmp_subject.start_h1 * 60 + tmp_subject.start_m1 >= subject.fin_h1 * 60 + subject.fin_m1 or tmp_subject.fin_h1 * 60 + tmp_subject.fin_m1 <= subject.start_h1 * 60 + subject.start_m1:
                            pass
                        else:
                            overlap = True
                            break
                    if tmp_subject.day1 == subject.day2:
                        if tmp_subject.start_h1 * 60 + tmp_subject.start_m1 >= subject.fin_h2 * 60 + subject.fin_m2 or tmp_subject.fin_h1 * 60 + tmp_subject.fin_m1 <= subject.start_h2 * 60 + subject.start_m2:
                            pass
                        else:
                            overlap = True
                            break
                    if tmp_subject.day2 == subject.day1:
                        if tmp_subject.start_h2 * 60 + tmp_subject.start_m2 >= subject.fin_h1 * 60 + subject.fin_m1 or tmp_subject.fin_h2 * 60 + tmp_subject.fin_m2 <= subject.start_h1 * 60 + subject.start_m1:
                            pass
                        else:
                            overlap = True
                            break
                    if tmp_subject.day2 == subject.day2:
                        if tmp_subject.start_h2 * 60 + tmp_subject.start_m2 >= subject.fin_h2 * 60 + subject.fin_m2 or tmp_subject.fin_h2 * 60 + tmp_subject.fin_m2 <= subject.start_h2 * 60 + subject.start_m2:
                            pass
                        else:
                            overlap = True
                            break
                    if tmp_subject.day3 == subject.day1:
                        if tmp_subject.start_h3 * 60 + tmp_subject.start_m3 >= subject.fin_h1 * 60 + subject.fin_m1 or tmp_subject.fin_h3 * 60 + tmp_subject.fin_m3 <= subject.start_h1 * 60 + subject.start_m1:
                            pass
                        else:
                            overlap = True
                            break
                    if tmp_subject.day3 == subject.day2:
                        if tmp_subject.start_h3 * 60 + tmp_subject.start_m3 >= subject.fin_h2 * 60 + subject.fin_m2 or tmp_subject.fin_h3 * 60 + tmp_subject.fin_m3 <= subject.start_h2 * 60 + subject.start_m2:
                            pass
                        else:
                            overlap = True
                            break
                    if tmp_subject.day4 == subject.day1:
                        if tmp_subject.start_h4 * 60 + tmp_subject.start_m4 >= subject.fin_h1 * 60 + subject.fin_m1 or tmp_subject.fin_h4 * 60 + tmp_subject.fin_m4 <= subject.start_h1 * 60 + subject.start_m1:
                            pass
                        else:
                            overlap = True
                            break
                    if tmp_subject.day4 == subject.day2:
                        if tmp_subject.start_h4 * 60 + tmp_subject.start_m4 >= subject.fin_h2 * 60 + subject.fin_m2 or tmp_subject.fin_h4 * 60 + tmp_subject.fin_m4 <= subject.start_h2 * 60 + subject.start_m2:
                            pass
                        else:
                            overlap = True
                            break
                elif subject.count == 3:
                    if tmp_subject.day1 == subject.day1:
                        if tmp_subject.start_h1 * 60 + tmp_subject.start_m1 >= subject.fin_h1 * 60 + subject.fin_m1 or tmp_subject.fin_h1 * 60 + tmp_subject.fin_m1 <= subject.start_h1 * 60 + subject.start_m1:
                            pass
                        else:
                            overlap = True
                            break
                    if tmp_subject.day1 == subject.day2:
                        if tmp_subject.start_h1 * 60 + tmp_subject.start_m1 >= subject.fin_h2 * 60 + subject.fin_m2 or tmp_subject.fin_h1 * 60 + tmp_subject.fin_m1 <= subject.start_h2 * 60 + subject.start_m2:
                            pass
                        else:
                            overlap = True
                            break
                    if tmp_subject.day1 == subject.day3:
                        if tmp_subject.start_h1 * 60 + tmp_subject.start_m1 >= subject.fin_h3 * 60 + subject.fin_m3 or tmp_subject.fin_h1 * 60 + tmp_subject.fin_m1 <= subject.start_h3 * 60 + subject.start_m3:
                            pass
                        else:
                            overlap = True
                            break
                    if tmp_subject.day2 == subject.day1:
                        if tmp_subject.start_h2 * 60 + tmp_subject.start_m2 >= subject.fin_h1 * 60 + subject.fin_m1 or tmp_subject.fin_h2 * 60 + tmp_subject.fin_m2 <= subject.start_h1 * 60 + subject.start_m1:
                            pass
                        else:
                            overlap = True
                            break
                    if tmp_subject.day2 == subject.day2:
                        if tmp_subject.start_h2 * 60 + tmp_subject.start_m2 >= subject.fin_h2 * 60 + subject.fin_m2 or tmp_subject.fin_h2 * 60 + tmp_subject.fin_m2 <= subject.start_h2 * 60 + subject.start_m2:
                            pass
                        else:
                            overlap = True
                            break
                    if tmp_subject.day2 == subject.day3:
                        if tmp_subject.start_h2 * 60 + tmp_subject.start_m2 >= subject.fin_h3 * 60 + subject.fin_m3 or tmp_subject.fin_h2 * 60 + tmp_subject.fin_m2 <= subject.start_h3 * 60 + subject.start_m3:
                            pass
                        else:
                            overlap = True
                            break
                    if tmp_subject.day3 == subject.day1:
                        if tmp_subject.start_h3 * 60 + tmp_subject.start_m3 >= subject.fin_h1 * 60 + subject.fin_m1 or tmp_subject.fin_h3 * 60 + tmp_subject.fin_m3 <= subject.start_h1 * 60 + subject.start_m1:
                            pass
                        else:
                            overlap = True
                            break
                    if tmp_subject.day3 == subject.day2:
                        if tmp_subject.start_h3 * 60 + tmp_subject.start_m3 >= subject.fin_h2 * 60 + subject.fin_m2 or tmp_subject.fin_h3 * 60 + tmp_subject.fin_m3 <= subject.start_h2 * 60 + subject.start_m2:
                            pass
                        else:
                            overlap = True
                            break
                    if tmp_subject.day3 == subject.day3:
                        if tmp_subject.start_h3 * 60 + tmp_subject.start_m3 >= subject.fin_h3 * 60 + subject.fin_m3 or tmp_subject.fin_h3 * 60 + tmp_subject.fin_m3 <= subject.start_h3 * 60 + subject.start_m3:
                            pass
                        else:
                            overlap = True
                            break
                    if tmp_subject.day4 == subject.day1:
                        if tmp_subject.start_h4 * 60 + tmp_subject.start_m4 >= subject.fin_h1 * 60 + subject.fin_m1 or tmp_subject.fin_h4 * 60 + tmp_subject.fin_m4 <= subject.start_h1 * 60 + subject.start_m1:
                            pass
                        else:
                            overlap = True
                            break
                    if tmp_subject.day4 == subject.day2:
                        if tmp_subject.start_h4 * 60 + tmp_subject.start_m4 >= subject.fin_h2 * 60 + subject.fin_m2 or tmp_subject.fin_h4 * 60 + tmp_subject.fin_m4 <= subject.start_h2 * 60 + subject.start_m2:
                            pass
                        else:
                            overlap = True
                            break
                    if tmp_subject.day4 == subject.day3:
                        if tmp_subject.start_h4 * 60 + tmp_subject.start_m4 >= subject.fin_h3 * 60 + subject.fin_m3 or tmp_subject.fin_h4 * 60 + tmp_subject.fin_m4 <= subject.start_h3 * 60 + subject.start_m3:
                            pass
                        else:
                            overlap = True
                            break
                elif subject.count == 4:
                    if tmp_subject.day1 == subject.day1:
                        if tmp_subject.start_h1 * 60 + tmp_subject.start_m1 >= subject.fin_h1 * 60 + subject.fin_m1 or tmp_subject.fin_h1 * 60 + tmp_subject.fin_m1 <= subject.start_h1 * 60 + subject.start_m1:
                            pass
                        else:
                            overlap = True
                            break
                    if tmp_subject.day1 == subject.day2:
                        if tmp_subject.start_h1 * 60 + tmp_subject.start_m1 >= subject.fin_h2 * 60 + subject.fin_m2 or tmp_subject.fin_h1 * 60 + tmp_subject.fin_m1 <= subject.start_h2 * 60 + subject.start_m2:
                            pass
                        else:
                            overlap = True
                            break
                    if tmp_subject.day1 == subject.day3:
                        if tmp_subject.start_h1 * 60 + tmp_subject.start_m1 >= subject.fin_h3 * 60 + subject.fin_m3 or tmp_subject.fin_h1 * 60 + tmp_subject.fin_m1 <= subject.start_h3 * 60 + subject.start_m3:
                            pass
                        else:
                            overlap = True
                            break
                    if tmp_subject.day1 == subject.day4:
                        if tmp_subject.start_h1 * 60 + tmp_subject.start_m1 >= subject.fin_h4 * 60 + subject.fin_m4 or tmp_subject.fin_h1 * 60 + tmp_subject.fin_m1 <= subject.start_h4 * 60 + subject.start_m4:
                            pass
                        else:
                            overlap = True
                            break
                    if tmp_subject.day2 == subject.day1:
                        if tmp_subject.start_h2 * 60 + tmp_subject.start_m2 >= subject.fin_h1 * 60 + subject.fin_m1 or tmp_subject.fin_h2 * 60 + tmp_subject.fin_m2 <= subject.start_h1 * 60 + subject.start_m1:
                            pass
                        else:
                            overlap = True
                            break
                    if tmp_subject.day2 == subject.day2:
                        if tmp_subject.start_h2 * 60 + tmp_subject.start_m2 >= subject.fin_h2 * 60 + subject.fin_m2 or tmp_subject.fin_h2 * 60 + tmp_subject.fin_m2 <= subject.start_h2 * 60 + subject.start_m2:
                            pass
                        else:
                            overlap = True
                            break
                    if tmp_subject.day2 == subject.day3:
                        if tmp_subject.start_h2 * 60 + tmp_subject.start_m2 >= subject.fin_h3 * 60 + subject.fin_m3 or tmp_subject.fin_h2 * 60 + tmp_subject.fin_m2 <= subject.start_h3 * 60 + subject.start_m3:
                            pass
                        else:
                            overlap = True
                            break
                    if tmp_subject.day2 == subject.day4:
                        if tmp_subject.start_h2 * 60 + tmp_subject.start_m2 >= subject.fin_h4 * 60 + subject.fin_m4 or tmp_subject.fin_h2 * 60 + tmp_subject.fin_m2 <= subject.start_h4 * 60 + subject.start_m4:
                            pass
                        else:
                            overlap = True
                            break
                    if tmp_subject.day3 == subject.day1:
                        if tmp_subject.start_h3 * 60 + tmp_subject.start_m3 >= subject.fin_h1 * 60 + subject.fin_m1 or tmp_subject.fin_h3 * 60 + tmp_subject.fin_m3 <= subject.start_h1 * 60 + subject.start_m1:
                            pass
                        else:
                            overlap = True
                            break
                    if tmp_subject.day3 == subject.day2:
                        if tmp_subject.start_h3 * 60 + tmp_subject.start_m3 >= subject.fin_h2 * 60 + subject.fin_m2 or tmp_subject.fin_h3 * 60 + tmp_subject.fin_m3 <= subject.start_h2 * 60 + subject.start_m2:
                            pass
                        else:
                            overlap = True
                            break
                    if tmp_subject.day3 == subject.day3:
                        if tmp_subject.start_h3 * 60 + tmp_subject.start_m3 >= subject.fin_h3 * 60 + subject.fin_m3 or tmp_subject.fin_h3 * 60 + tmp_subject.fin_m3 <= subject.start_h3 * 60 + subject.start_m3:
                            pass
                        else:
                            overlap = True
                            break
                    if tmp_subject.day3 == subject.day4:
                        if tmp_subject.start_h3 * 60 + tmp_subject.start_m3 >= subject.fin_h4 * 60 + subject.fin_m4 or tmp_subject.fin_h3 * 60 + tmp_subject.fin_m3 <= subject.start_h4 * 60 + subject.start_m4:
                            pass
                        else:
                            overlap = True
                            break
                    if tmp_subject.day4 == subject.day1:
                        if tmp_subject.start_h4 * 60 + tmp_subject.start_m4 >= subject.fin_h1 * 60 + subject.fin_m1 or tmp_subject.fin_h4 * 60 + tmp_subject.fin_m4 <= subject.start_h1 * 60 + subject.start_m1:
                            pass
                        else:
                            overlap = True
                            break
                    if tmp_subject.day4 == subject.day2:
                        if tmp_subject.start_h4 * 60 + tmp_subject.start_m4 >= subject.fin_h2 * 60 + subject.fin_m2 or tmp_subject.fin_h4 * 60 + tmp_subject.fin_m4 <= subject.start_h2 * 60 + subject.start_m2:
                            pass
                        else:
                            overlap = True
                            break
                    if tmp_subject.day4 == subject.day3:
                        if tmp_subject.start_h4 * 60 + tmp_subject.start_m4 >= subject.fin_h3 * 60 + subject.fin_m3 or tmp_subject.fin_h4 * 60 + tmp_subject.fin_m4 <= subject.start_h3 * 60 + subject.start_m3:
                            pass
                        else:
                            overlap = True
                            break
                    if tmp_subject.day4 == subject.day4:
                        if tmp_subject.start_h4 * 60 + tmp_subject.start_m4 >= subject.fin_h4 * 60 + subject.fin_m4 or tmp_subject.fin_h4 * 60 + tmp_subject.fin_m4 <= subject.start_h4 * 60 + subject.start_m4:
                            pass
                        else:
                            overlap = True
                            break

        if overlap:
            messages.error(request, '시간표가 겹칩니다!!', ['선택한 강의 -> ID:' , tmp_subject.id, 'Name:', tmp_subject.name])
        else:
            tmp = Subject_add()
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
        temp = Subject_add.objects.filter(subject_add_id=subject_id, user_id = request.user.id)
        temp.delete()
    return redirect('timetable:mytable', user_id=request.user.id)


# def data_save(request):
#     # 엑셀파일 받기
#     Location = 'C:/Users/이주찬/Desktop/rmathing/mop_rm/juchan_time/timesite(0206_save_at_database)'
#     # 이거 바꿔줄 필요 있음
#     File = 'Excel_Timetable.xls'
#
#     data_pd = pd.read_excel('{}/{}'.format(Location, File),
#                             header=None, index_col=None, names=None)
#     time = []
#
#     # 시간정보 읽어오기
#     for i in range(1, len(data_pd)):
#         time.append(re.findall("\d+", str(data_pd[11][i])))
#     for i in range(len(time)):
#         time[i] = numpy.array(time[i]).reshape(len(time[i]) // 4, 2, 2)
#
#     # 요일정보 읽어오기
#     day = []
#     for i in range(1, len(data_pd)):
#         day.append(re.compile("[가-힣]+").findall(str(data_pd[11][i])))
#
#     # 교수님정보 읽어오기
#     prof = []
#     for i in range(1, len(data_pd)):
#         prof.append(re.compile("[가-힣]+").findall(str(data_pd[8][i])))
#
#     # 과목명 읽어오기
#     sub = []
#     for i in range(1, len(data_pd)):
#         sub.append(data_pd[5][i])
#
#     # 과목코드 읽어오기
#     code = []
#     for i in range(1, len(data_pd)):
#         code.append(data_pd[4][i])
#
#     # 학점정보 읽어오기
#     credit = []
#     for i in range(1, len(data_pd)):
#         credit.append(int(data_pd[27][i]))
#
#     #개설부서
#     department = []
#     for i in range(1, len(data_pd)):
#         department.append(data_pd[3][i])
#
#     #필수여부
#     is_required = []
#     for i in range(1, len(data_pd)):
#         is_required.append(data_pd[6][i])
#
#     #교양, 전공
#     is_major = []
#     for i in range(1, len(data_pd)):
#         is_major.append(data_pd[7][i])
#
#
#     for i in range(len(data_pd) - 1):
#         subject = SubjectInfo(name=sub[i], code=code[i], credit=credit[i], department=department[i], is_required=is_required[i], is_major=is_major[i])
#         if (len(prof[i]) == 1):
#             subject.professor1 = prof[i][0]
#         elif (len(prof[i]) == 2):
#             subject.professor1 = prof[i][0]
#             subject.professor2 = prof[i][1]
#
#         if (len(day[i]) == 1):
#             subject.day1 = day[i][0]
#             subject.start_time1 = time[i][0][0][0] + ":" + time[i][0][0][1]
#             subject.finish_time1 = time[i][0][1][0] + ":" + time[i][0][1][1]
#             subject.start_h1 = int(time[i][0][0][0])
#             subject.start_m1 = int(time[i][0][0][1])
#
#             subject.fin_h1 = int(time[i][0][1][0])
#             subject.fin_m1 = int(time[i][0][1][1])
#             subject.count = 1
#
#         elif (len(day[i]) == 2):
#             subject.day1 = day[i][0]
#             subject.day2 = day[i][1]
#             subject.start_time1 = time[i][0][0][0] + ":" + time[i][0][0][1]
#             subject.start_time2 = time[i][1][0][0] + ":" + time[i][1][0][1]
#             subject.finish_time1 = time[i][0][1][0] + ":" + time[i][0][1][1]
#             subject.finish_time2 = time[i][1][1][0] + ":" + time[i][1][1][1]
#             subject.start_h1 = int(time[i][0][0][0])
#             subject.start_m1 = int(time[i][0][0][1])
#             subject.fin_h1 = int(time[i][0][1][0])
#             subject.fin_m1 = int(time[i][0][1][1])
#             subject.start_h2 = int(time[i][1][0][0])
#             subject.start_m2 = int(time[i][1][0][1])
#             subject.fin_h2 = int(time[i][1][1][0])
#             subject.fin_m2 = int(time[i][1][1][1])
#             subject.count = 2
#
#         elif (len(day[i]) == 3):
#             subject.day1 = day[i][0]
#             subject.day2 = day[i][1]
#             subject.day3 = day[i][2]
#             subject.start_time1 = time[i][0][0][0] + ":" + time[i][0][0][1]
#             subject.start_time2 = time[i][1][0][0] + ":" + time[i][1][0][1]
#             subject.start_time3 = time[i][2][0][0] + ":" + time[i][2][0][1]
#             subject.finish_time1 = time[i][0][1][0] + ":" + time[i][0][1][1]
#             subject.finish_time2 = time[i][1][1][0] + ":" + time[i][1][1][1]
#             subject.finish_time3 = time[i][2][1][0] + ":" + time[i][2][1][1]
#             subject.start_h1 = int(time[i][0][0][0])
#             subject.start_m1 = int(time[i][0][0][1])
#             subject.fin_h1 = int(time[i][0][1][0])
#             subject.fin_m1 = int(time[i][0][1][1])
#             subject.start_h2 = int(time[i][1][0][0])
#             subject.start_m2 = int(time[i][1][0][1])
#             subject.fin_h2 = int(time[i][1][1][0])
#             subject.fin_m2 = int(time[i][1][1][1])
#             subject.start_h3 = int(time[i][2][0][0])
#             subject.start_m3 = int(time[i][2][0][1])
#             subject.fin_h3 = int(time[i][2][1][0])
#             subject.fin_m3 = int(time[i][2][1][1])
#             subject.count = 3
#
#         elif (len(day[i]) == 4):
#             subject.day1 = day[i][0]
#             subject.day2 = day[i][1]
#             subject.day3 = day[i][2]
#             subject.day4 = day[i][3]
#             subject.start_time1 = time[i][0][0][0] + ":" + time[i][0][0][1]
#             subject.start_time2 = time[i][1][0][0] + ":" + time[i][1][0][1]
#             subject.start_time3 = time[i][2][0][0] + ":" + time[i][2][0][1]
#             subject.start_time4 = time[i][3][0][0] + ":" + time[i][3][0][1]
#             subject.finish_time1 = time[i][0][1][0] + ":" + time[i][0][1][1]
#             subject.finish_time2 = time[i][1][1][0] + ":" + time[i][1][1][1]
#             subject.finish_time3 = time[i][2][1][0] + ":" + time[i][2][1][1]
#             subject.finish_time4 = time[i][3][1][0] + ":" + time[i][3][1][1]
#             subject.start_h1 = int(time[i][0][0][0])
#             subject.start_m1 = int(time[i][0][0][1])
#             subject.fin_h1 = int(time[i][0][1][0])
#             subject.fin_m1 = int(time[i][0][1][1])
#             subject.start_h2 = int(time[i][1][0][0])
#             subject.start_m2 = int(time[i][1][0][1])
#             subject.fin_h2 = int(time[i][1][1][0])
#             subject.fin_m2 = int(time[i][1][1][1])
#             subject.start_h3 = int(time[i][2][0][0])
#             subject.start_m3 = int(time[i][2][0][1])
#             subject.fin_h3 = int(time[i][2][1][0])
#             subject.fin_m3 = int(time[i][2][1][1])
#             subject.start_h4 = int(time[i][3][0][0])
#             subject.start_m4 = int(time[i][3][0][1])
#             subject.fin_h4 = int(time[i][3][1][0])
#             subject.fin_m4 = int(time[i][3][1][1])
#             subject.count = 4
#         subject.save()
#
#     return render(request, 'timetable/main.html')

