from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [
    path('list/', views.student_list, name='list'),
    path('detail/<int:student_id>/', views.student_detail, name='detail'),
]

