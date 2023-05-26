from django.views.decorators.csrf import csrf_exempt

from shared.dtos.response.errors import PageNotFoundErrorDto
from shared.response.basic import PageNotFoundResponse


# Create your views here.

@csrf_exempt
def page_not_found(request, exception=None):
    return PageNotFoundResponse(PageNotFoundErrorDto())
