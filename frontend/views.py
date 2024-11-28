from django.shortcuts import render ,redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from userEx.views import *
# Create your views here.
def home(request):
    user=request.user
    user=getUserEx(user)

    if user.is_authenticated:

        return render(request, 'index.html')
    else:
        return redirect('loginUser')
@login_required
def profile(request):
    return render(request, 'profile.html')
def loginUser(request):
    return render(request, 'login.html')
def register(request):
    return render(request, 'signup.html')
def user_logout(request):
    logout(request)
    return redirect('loginUser')

def notFound(request):
    return render(request, 'notfound.html')
