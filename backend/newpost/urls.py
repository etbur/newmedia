from django.urls import path
# from rest_framework.routers import DefaultRouter
from . import views
urlpatterns=[
  path('posts',views.PostViewSet.as_view(
    {'get': 'list'}
  ) ,name='posts'),
]