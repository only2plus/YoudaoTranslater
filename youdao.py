#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hashlib import md5
from random import randint
from requests import get


class Youdao:
    API_URL = 'http://openapi.youdao.com/api'
    APP_KEY = '5c9ff6cd28a58498'
    APP_SEC = '0WOi4190sDWm0bfbGXSdBCMmQ6z2kVZt'

    def request(self, q):
        salt = str(randint(1, 100))
        key = self.APP_KEY
        secret = self.APP_SEC
        sign = md5((key + q + salt + secret).encode()).hexdigest().upper()

        params = {
            'q': q,
            'from': 'auto',
            'to': 'auto',
            'appKey': key,
            'salt': salt,
            'sign': sign,
        }

        json = get(self.API_URL, params=params).json()

        if json['errorCode'] != '0':
            # http://ai.youdao.com/docs/doc-trans-api.s#p06
            text = 'error {}'.format(json['errorCode'])
        elif 'query' in json and 'basic' in json:
            text = '{}\n{}'.format(json['query'], '\n'.join(json['basic']['explains']))
        else:
            text = '{}\n{}'.format(json['query'], 'no translation')
        return text
