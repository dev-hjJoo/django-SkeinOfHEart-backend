from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from rest_framework.decorators import api_view
import requests
import json
from SOH.models import Page, User, LabelContent

""" 공공 API 사용 함수 """


def get_emotion_score(content):
    # URL 지정
    url = 'http://svc.saltlux.ai:31781'

    # Header 정보 지정
    headers = {'Content-Type': 'application/json; charset=utf-8'}

    # Request Parameter 정보 지정
    params = {
        "key": "6f68cfc9-9443-4f4b-9b73-d766d02b566d",
        "serviceId": "11987300804",
        "argument": {
            "type": "0",
            "query": content
        }
    }

    response = requests.post(url, headers=headers,
                             data=json.dumps(params)).json()

    return response['label']


def get_emotion_state(content):
    # URL 지정
    url = 'http://svc.saltlux.ai:31781'

    # Header 정보 지정
    headers = {'Content-Type': 'application/json; charset=utf-8'}

    # Request Parameter 정보 지정
    params = {
        "key": "6f68cfc9-9443-4f4b-9b73-d766d02b566d",
        "serviceId": "11987300804",
        "argument": {
            "type": "1",
            "query": content
        }
    }

    response = requests.post(url, headers=headers,
                             data=json.dumps(params)).json()

    return response['Result'][0][1]


@api_view(['POST'])
def save_page(request):
    diary_no = request.POST.get('diary_no', False)
    topic_no = request.POST.get('topic_no', False)
    user_no = request.POST.get('user_no', False)
    content = request.POST.get('content', False)

    if diary_no == False:
        return HttpResponseNotFound('diary_no 전달되지 않음')
    if topic_no == False:
        return HttpResponseNotFound('topic_no 전달되지 않음')
    if user_no == False:
        return HttpResponseNotFound('user_no 전달되지 않음')
    if content == False:
        return HttpResponseNotFound('content 전달되지 않음')

    emo_state = get_emotion_state(content)
    emo_pos = 0 if get_emotion_score(content) == '긍정' else 1

    page = Page(diary_no=diary_no, user_no=user_no, topic_no=topic_no, content=content, emotion_score=emo_pos, emotion_state=emo_state)
    page.save()

    labelContent = LabelContent(content=content, emotion_score=emo_pos, emotion_state=emo_state)
    labelContent.save()

    return HttpResponse('okay', content_type="application/json")


@api_view(['POST'])
def save_user(request):
    name = request.POST.get('name', False)
    age = request.POST.get('age', False)
    id = request.POST.get('id', False)
    password = request.POST.get('password', False)
    if name == False:
        return HttpResponseNotFound('name 전달되지 않음')
    if age == False:
        return HttpResponseNotFound('age 전달되지 않음')
    if id == False:
        return HttpResponseNotFound('id 전달되지 않음')
    if password == False:
        return HttpResponseNotFound('password 전달되지 않음')

    user = User(name=name, age=age, id=id, password=password)
    user.save()

    return HttpResponse('okay', content_type="application/json")
