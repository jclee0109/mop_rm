from django.http import HttpResponse
# ---------------------------------- [edit] ---------------------------------- #
from .models import Question
# ---------------------------------------------------------------------------- #


def index(request):
    """
    pybo
    """





    return HttpResponse("안녕하세요 pybo에 온 것을 환영합니다.")
