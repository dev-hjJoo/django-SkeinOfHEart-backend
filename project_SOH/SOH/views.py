from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from rest_framework.decorators import api_view

from .models import LabelContent

from konlpy.tag import Okt  # 형태소 분석기 (말뭉치)
import re  # 문자열 정규표현식 지원 모듈
from collections import Counter # 형태소 개수 세기
import requests
import json
from hanspell import spell_checker


""" 전처리 함수 """
def textTokenizer(content):
    okt = Okt()
    # 형태소별 자른 토큰 리스트
    tokens = []

    # 불용어 처리
    stop_words = ['함초롬바탕', '고딕']
    content = re.sub(r'[^ ㄱ-ㅣ가-힣]', '', content)
    tokens = okt.pos(content, stem=True)
    # 불용어가 아니고, 동/명/형/한국 파티클(ex_ㅋㅋ)
    tokens = [each_word for (each_word, each_pos) in tokens if each_word not in stop_words and each_pos in ('Noun', 'Adjective', 'Verb', 'KoreanParticle')]

    return tokens

def makeFormForWordcloud(dic):
    result = []
    for key, value in dic.items():
        innerValue = {}
        innerValue["text"] = key
        innerValue["value"] = value
        result.append(innerValue)
    return result




# API 함수/클래스
@api_view(['POST'])
def make_wordcloud(request):
    content = request.POST.get('content', False)

    if content == False:
        return HttpResponseNotFound('content 전달되지 않음')

    tokens = textTokenizer(content)
    count = Counter(tokens)
    result = makeFormForWordcloud(dict(count))

    return HttpResponse(json.dumps(result, indent=4), content_type="application/json")

@api_view(['POST'])
def correct_content(request):
    content = request.POST.get('content', False)
    result = spell_checker.check(content)
    result = result.as_dict()

    return HttpResponse(json.dumps(result['checked']), content_type="application/json")


@api_view(['POST'])
def test(request):
    data = request.POST.get('content')
    return HttpResponse(data)
