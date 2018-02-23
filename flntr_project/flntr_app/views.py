from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse

# Create your views here.
def index(request):
    return render(request, 'flntr/index.html')

def about(request):
    return render(request, 'flntr/about.html')

def search(request):
    return render(request, 'flntr/search.html')

def register(request):
    return render(request, 'flntr/register.html')

def user_login(request):
    return render(request, 'flntr/login.html')

def property(request):
    return render(request, 'flntr/property.html')

def show_property(request):
    return render(request, 'flntr/show_property.html')

def user(request):
    return render(request, 'flntr/user.html')

def show_user(request):
    return render(request, 'flntr/show_user.html')

def show_user_invitations(request):
    return render(request, 'flntr/show_user_invitations.html')

def show_user_requests(request):
    return render(request, 'flntr/show_user_requests.html')

def show_user_account(request):
    return render(request, 'flntr/show_user_account.html')

def show_user_profile(request):
    return render(request, 'flntr/show_user_profile.html')

def show_user_properties(request):
    return render(request, 'flntr/show_user_properties.html')

def show_user_properties_aProperty(request):
    return render(request, 'flntr/show_user_properties_aProperties.html')

def user_logout(request):
    return render(request, 'flntr/user_logout.html')
