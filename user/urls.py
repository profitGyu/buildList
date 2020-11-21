from django.urls import path

from user.views import UserRegisterationView

# as_view() 메소드의 역할 뷰클래스의 초기화와 핸들러를 반환하는 기능
urlpatterns = [
    path('create/', UserRegisterationView.as_view(), name="user_create")
]