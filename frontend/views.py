from django.shortcuts import render ,redirect
from django.contrib.auth import logout
# Create your views here.
def home(request):
    return render(request, 'index.html')
def profile(request):
    return render(request, 'profile.html')
def loginUser(request):
    return render(request, 'login.html')
def register(request):
    return render(request, 'signup.html')
def user_logout(request):
    logout(request)
    return redirect('loginUser')
