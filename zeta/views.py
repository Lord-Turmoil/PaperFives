from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
def sample(request):
    if request.method == "POST":
        return JsonResponse({"Invalid request"})
    return render(request, 'welcome.html')