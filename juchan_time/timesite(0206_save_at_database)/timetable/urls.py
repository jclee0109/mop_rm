from django.urls import path

from . import views

app_name = 'timetable'

urlpatterns = [
    path('', views.main, name = 'main'),
    path('<int:user_id>/',views.mytable, name = 'mytable'),
    path('choice/subject/<int:subject_id>/<int:user_id>', views.choice_subject, name='choice_subject'),
    # path('choice/add/<int:subject_id>/', views.subject_add, name='subject_add'),
    path('data/',views.data_save, name = 'data_save'),
]