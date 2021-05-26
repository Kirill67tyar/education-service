from django.shortcuts import render
from django.http import JsonResponse

from courses.utils import get_view_at_console1


def experiments_view(request):
    get_view_at_console1(request.session)
    return JsonResponse({'status': 'ok', })
