from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('<str:entity>', views.entity, name='posts'),
    path('<str:entity>/<str:id>', views.entity_by_id, name='posts'),

]
