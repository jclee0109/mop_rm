from django.shortcuts import render
from .models import SubjectInfo
# ---------------------------------------------------------------------------- #

def main(request):
    """
    강의 목록 출력
    """
    subject_list = SubjectInfo.objects.order_by('name')
    context = {'subject_list': subject_list}
    return render(request, 'main.html', context)
