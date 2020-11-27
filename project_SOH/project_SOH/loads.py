from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from rest_framework.decorators import api_view

from SOH.models import Page
import json


@api_view(['POST'])
def load_pages(request):
    user_no = request.POST.get('user_no', False)

    if user_no == False:
        return HttpResponseNotFound('user_no 전달되지 않음')

    result = Page.objects.filter(user_no=user_no).values('content', 'emotion_score', 'emotion_state', 'datetime')
    result = list(result)
    for temp in result:
        temp['datetime'] = temp['datetime'].strftime('%Y-%m-%d')

    return HttpResponse(json.dumps(result), content_type="application/json")
