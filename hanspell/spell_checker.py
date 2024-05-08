# -*- coding: utf-8 -*-
"""
Python용 한글 맞춤법 검사 모듈
"""

import requests
import json
import time
import sys
from collections import OrderedDict
import xml.etree.ElementTree as ET

from .response import Checked
from .constants import base_url
from .constants import CheckResult

_agent = requests.Session()
PY3 = sys.version_info[0] == 3


def _remove_tags(text):
    import re
    # 모든 HTML 태그 제거
    text = re.sub(r'<[^>]+>', '', text)
    return text


def check(text):
    """
    매개변수로 입력받은 한글 문장의 맞춤법을 체크합니다.
    """
    if isinstance(text, list):
        result = []
        for item in text:
            checked = check(item)
            result.append(checked)
        return result

    # 최대 500자까지 가능.
    if len(text) > 500:
        return Checked(result=False)

    payload = {
        'color_blindness': '0',
        'q': text,
        'passportKey': '069f818f3885981d5857c57c6f6b0fd96578391b',
        '_callback': 'jQuery112405442127330168605_1715140858749'
    }

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
        'referer': 'https://search.naver.com/',
    }

    start_time = time.time()
    r = _agent.get(base_url, params=payload, headers=headers)
    passed_time = time.time() - start_time

    # data = json.loads(r.text)
    
    import re

    json_data = re.search(r'\((.*)\)', r.text).group(1)
    data = json.loads(json_data)

    print("data", data)
    
    html = data['message']['result']['html']
    result = {
        'result': True,
        'original': text,
        'checked': _remove_tags(html),
        'errors': data['message']['result']['errata_count'],
        'time': passed_time,
        'words': OrderedDict(),
    }

    # 띄어쓰기로 구분하기 위해 태그는 일단 보기 쉽게 바꿔둠.
    # ElementTree의 iter()를 써서 더 좋게 할 수 있는 방법이 있지만
    # 이 짧은 코드에 굳이 그렇게 할 필요성이 없으므로 일단 문자열을 치환하는 방법으로 작성.
    html = html.replace('<em class=\'green_text\'>', '<green>') \
               .replace('<em class=\'red_text\'>', '<red>') \
               .replace('<em class=\'violet_text\'>', '<violet>') \
               .replace('<em class=\'blue_text\'>', '<blue>') \
               .replace('</em>', '<end>')
    items = html.split(' ')
    words = []
    tmp = ''
    for word in items:
        if tmp == '' and word[:1] == '<':
            pos = word.find('>') + 1
            tmp = word[:pos]
        elif tmp != '':
            word = u'{}{}'.format(tmp, word)
        
        if word[-5:] == '<end>':
            word = word.replace('<end>', '')
            tmp = ''

        words.append(word)

    
    modifications = []
    for word in words:
        check_result = CheckResult.PASSED
        if word[:5] == '<red>':
            check_result = CheckResult.WRONG_SPELLING
            word = word.replace('<red>', '')
            modifications.append(word)
        elif word[:7] == '<green>':
            check_result = CheckResult.WRONG_SPACING
            word = word.replace('<green>', '')
            modifications.append(word)
        # elif word[:8] == '<violet>':
        #     check_result = CheckResult.AMBIGUOUS
        #     word = word.replace('<violet>', '')
        # elif word[:6] == '<blue>':
        #     check_result = CheckResult.STATISTICAL_CORRECTION
        #     word = word.replace('<blue>', '')
        result['words'][word] = check_result

    result['modifications'] = modifications
    result = Checked(**result)

    return result
