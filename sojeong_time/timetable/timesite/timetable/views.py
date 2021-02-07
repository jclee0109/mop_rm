from django.shortcuts import render, redirect
from .models import SubjectInfo, UserChoice


def main(request):
    """
    강의 목록 출력
    """
    subject_list = SubjectInfo.objects.order_by('id')
    context = {'subject_list': subject_list}
    return render(request, 'main.html', context)


def add(request, subject_id):
    """
    과목 추가
    """
    if request.method == 'GET':
        temp = UserChoice()
        temp_subject = SubjectInfo.objects.get(id=subject_id)
        temp.subject_selected = temp_subject
        temp.subject_selected_id = subject_id
        temp.save()
    return redirect('timetable:main')


def dele(request, subject_id):
    """
    과목 삭제
    """
    if request.method == 'GET':
        temp = UserChoice.objects.get(subject_selected_id=subject_id)
        temp.delete()
    return redirect('timetable:main')





