from django.urls import path

from . import views
app_name = 'timetable'

urlpatterns = [
    path('', views.main, name='main'),
    path('add/<int:subject_id>', views.add, name='add'),
    path('del/<int:subject_id>', views.dele, name='del'),

]




