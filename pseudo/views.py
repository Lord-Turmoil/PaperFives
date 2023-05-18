from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


# Create your views here.

@csrf_exempt
def sample(request):
    if request.method == "POST":
        return JsonResponse({"Invalid request"})
    return render(request, 'welcome.html')


@csrf_exempt
def login(request):
    return render(request, 'login.html')

@csrf_exempt
def register(request):
    return render(request, 'register.html')
