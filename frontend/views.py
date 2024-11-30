from django.shortcuts import render ,redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import JsonResponse
from userEx.views import *
import requests
# Create your views here.
def home(request):
    user=request.user
    if user.is_authenticated:
        user=getUserEx(user)
        user_ex=UserEx.objects.get(id=user.id)
        
        context={
            "name" : user_ex.first_name,
            "email":user_ex.email,
            'profile_image': user.profile_image.url if user.profile_image else None,

        }
        return render(request, 'index.html',context)
    else:
        return redirect('loginUser')
#======== Update API Handle ====================
# @login_required
def profile(request):
    user = request.user
    if user.is_authenticated:
        user = getUserEx(user)
        user_ex = UserEx.objects.get(id=user.id)
        if request.method == 'POST':
            status_input = request.POST.get('status')
            name_input = request.POST.get('name')
            profile_image_input = request.FILES.get('profile_image')
            data = {
                'status': status_input,
                'full_name': name_input,
            }
            files = {
                'profile_image': profile_image_input,
            } if profile_image_input else {}
            api_url = f'http://127.0.0.1:8000/users/get/{user.id}/' 
            try:
                response = requests.patch(api_url, data=data, files=files)
                if response.status_code == 200:
                    return redirect('profile')
                else:
                    return JsonResponse({'error': 'Failed to update profile.'}, status=400)
            except requests.exceptions.RequestException as e:
                return JsonResponse({'error': str(e)}, status=500)
        context = {
            "name" : user_ex.first_name,
            'status': user_ex.status,
            'profile_image': user_ex.profile_image.url if user_ex.profile_image else None
        }
        return render(request, 'profile.html', context)
def loginUser(request):
    return render(request, 'login.html')
def register(request):
    return render(request, 'signup.html')
def user_logout(request):
    logout(request)
    return redirect('loginUser')

def notFound(request):
    return render(request, 'notfound.html')
