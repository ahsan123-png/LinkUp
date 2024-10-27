from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'index.html')
def profile(request):
    return render(request, 'profile.html')
def loginUser(request):
    return render(request, 'login.html')
def register(request):
    return render(request, 'signup.html')