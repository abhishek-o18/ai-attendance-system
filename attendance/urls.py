from django.urls import path
from . import views

app_name = 'attendance'

urlpatterns = [
    path('mark/', views.mark_attendance, name='mark'),
    path('update/<int:class_id>/<str:date>/', views.update_attendance, name='update'),
    path('history/', views.attendance_history, name='history'),
    path('view/<int:class_id>/<str:date>/', views.view_attendance, name='view'),
    path("biometric/", views.biometric_receive, name="biometric_receive"),
    path("", views.biometric_receive),
    path("iclock/cdata", views.biometric_receive),
    path('start-face/<int:class_id>/', views.start_face_attendance, name='start_face'),
]

# from django.urls import path
# from . import views

# app_name = 'attendance'

# urlpatterns = [
#     path('mark/', views.mark_attendance, name='mark'),
#     path('update/<int:class_id>/<str:date>/', views.update_attendance, name='update'),
#     path('history/', views.attendance_history, name='history'),
#     path('view/<int:class_id>/<str:date>/', views.view_attendance, name='view'),

#     # ✅ biometric routes
#     path("biometric/", views.biometric_receive, name="biometric_receive"),
#     path("iclock/cdata", views.biometric_receive),  # 👈 MACHINE USE KAREGI
# ]