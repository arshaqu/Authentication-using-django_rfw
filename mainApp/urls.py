from django.urls import path
from .views import *

urlpatterns = [
    path('task/',TaskListview.as_view(),name='tasks'),
    path('task/<int:pk>/',TaskListview.as_view(),name='task-details'),
    path('task/create/',TaskListview.as_view(),name='task-create'),
    path('task/update/<int:pk>/',TaskListview.as_view(),name='task-update'),
    path('task/delete/<int:pk>/',TaskListview.as_view(),name='task-delete')
]