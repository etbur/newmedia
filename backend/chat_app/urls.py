from django.urls import path, include
from rest_framework.routers import DefaultRouter

from chat_app.views.auth_view import *
from rest_framework.authtoken import views

from chat_app.views.call_view import StartCall, EndCall
from chat_app.views.message_view import MessageView
from chat_app.views.post_view import PostViewSet
from chat_app.views.student_view import StudentList, StudentCreate
from backend import settings

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')

urlpatterns = [
    path('api-token-auth/', views.obtain_auth_token),
    path('login/', Login.as_view()),
    path('registration/', RegisterView.as_view()),
    path('logout/', LogOutView.as_view()),
    path('users/', UsersView.as_view()),
    path('message/', MessageView.as_view()),
    path('start-call/', StartCall.as_view()),
    path('end-call/', EndCall.as_view()),
    path('test-socket/', test_socket),
    path('student/', StudentList.as_view()),
    path('StudentCreate/', StudentCreate.as_view()),
    path('', include(router.urls)),
    # path('postview/',PostViewSet.as_view())
]
