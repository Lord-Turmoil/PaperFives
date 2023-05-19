from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from shared.dtos.response.users import UserProfileDto
from shared.utils.users.users import get_user_from_request
from users.serializer import UserSerializer
from shared.utils.json_util import serialize, deserialize


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
def logout(request):
    return render(request, 'logout.html')


@csrf_exempt
def register(request):
    return render(request, 'register.html')


@csrf_exempt
def profile(request):
    user = get_user_from_request(request)
    if user is None:
        return render(request, 'not_logged_in.html')
    data = deserialize(serialize(UserProfileDto(UserSerializer(user).data)))
    print(data)
    return render(request, 'profile.html', data)
