# -*- coding: utf-8 -*-
import base64
import requests

iv = 'UGFkT3JhY2xlOml2L2NiY8O+7uQmXKFqNVUuI9c7VBe42FqRvernmQhsxyPnvxaF'.decode('base64')[:16]
cipher_origin = 'UGFkT3JhY2xlOml2L2NiY8O+7uQmXKFqNVUuI9c7VBe42FqRvernmQhsxyPnvxaF'.decode('base64')
cipher = 'UGFkT3JhY2xlOml2L2NiY8O+7uQmXKFqNVUuI9c7VBe42FqRvernmQhsxyPnvxaF'.decode('base64')[16:]

print (iv + cipher[:16]).encode("base64")

old = 'dmin":false}' + 4 * "\x04"
new = 'dmin":true}' + 5 * "\x05"
tmp = ''
for i in range(16):
    tmp += chr(ord(old[i]) ^ ord(new[i]) ^ ord(cipher[i]))
out = tmp + cipher[16:]
ss = '{"id":104,"roleA'
new_iv = ""
ss2 = "00df71d27118c10e13141c66fc84619b".decode('hex') # 这个需要padding oracle出来~ @angelwhu
for i in range(16):
    new_iv += chr(ord(ss[i]) ^ ord(ss2[i]))
print base64.b64encode(new_iv + out)

#
# from Crypto.Util.strxor import strxor
# from base64 import *
# import requests
#
# str = 'UGFkT3JhY2xlOml2L2NiY8O+7uQmXKFqNVUuI9c7VBe42FqRvernmQhsxyPnvxaF'
# token = b64decode(str)
# iv = token[:16]
# C1 = token[16:32]
# C2 = token[32:]
# raw_iv = 'PadOracle:iv/cbc'
# json = '{"id":100,"roleAdmin":false}'
# D_C1 = strxor(json[:16], raw_iv)
# cipher = strxor(strxor(iv, json[:16]), '{"roleAdmin":1,"') + C1 + strxor(D_C1, '":"1","id":001}' + chr(1)) + C1
# cipher = b64encode(cipher)
