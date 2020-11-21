from django.shortcuts import render

# Create your views here.
from django.views.generic import CreateView
from user.models import User

class UserRegisterationView(CreateView):
    model = User
    fields = ('email', 'name', 'password')