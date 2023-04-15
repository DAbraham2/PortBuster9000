#  MIT License
#
#  Copyright (c) 2023 Daniel Abraham - daniel.abraham@edu.bme.hu
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.

#  MIT License
#
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#
import logging
import socket
import time

import requests as requests
import urllib3

from .solver import secrecy, math

logger = logging.getLogger(__name__)

NEPTUN_TO_EXTEND: str = ''


def task_EncryptHash(soc: socket.socket) -> socket.socket:
    """
    A kővetkező lépésben el kell küldeni a szerver részére a neptun kód és
    az utolsó feladvány eredményének az összefűzéséből keletkezett string
    SHA1 hashét. Pl.:\n
    \n
    Now give me the (lowercase) sha1 hash of your neptun\n
    concatenated with the last result!\n
    sha1(’NEPTUN-10001’):

    :param soc:
    :return:
    """
    global NEPTUN_TO_EXTEND
    time.sleep(0.3)
    rec = str(soc.recv(1024), 'utf-8')
    logger.info(f'Received: {rec}')
    challenge = rec.splitlines()
    if len(challenge) == 3 and challenge[1].startswith('Now give me'):
        last_index = challenge[2].find('\'', 7)
        NEPTUN_TO_EXTEND = challenge[2][6:last_index]
        enc = secrecy.encrypt_str(NEPTUN_TO_EXTEND)
        soc.send(bytes(enc, 'utf-8'))
    else:
        logger.error('Incorrect format')
        exit(4)

    return soc


def task_SolveExtend(soc: socket.socket) -> socket.socket:
    """
    A következő lépésben a szerver egy kihívást küld a kliens felé ilyen formában: \n
    Now extend ’NEPTUN-10001’ so that sha1(’NEPTUN-10001’+x) begins with ’0000’!\n
    The data should contain only printable characters.\n
    Data:\n
    :param soc:
    :return:
    """
    time.sleep(0.5)
    rec = str(soc.recv(1024), 'utf-8')
    logger.info(f'Received: {rec}')
    challenge = rec.split('\n')
    if len(challenge) == 3 and challenge[0].startswith('Now extend'):
        text, _hash = math.roll_dem_dice(NEPTUN_TO_EXTEND)
        soc.send(bytes(text, 'utf-8'))
    else:
        logger.error('Incorrect format')
        exit(5)

    return soc


def task_navigate_web(soc: socket.socket) -> None:
    urllib3.disable_warnings()

    url = 'http://152.66.249.144'
    s = requests.Session()
    r = s.post(url, data={'neptun': 'DASGYJ', 'password': 'crysys'})
    logger.debug(r.text)
    cert = s.get(url + '/getcert.php')
    logger.debug(cert.content)
    open('clientcert.pem', 'wb').write(cert.content)
    key = s.get(url + '/getkey.php')
    logger.debug(key.content)
    open('clientkey.pem', 'wb').write(key.content)
    response = requests.get('https://152.66.249.144', cert=('clientcert.pem', 'clientkey.pem'), verify=False,
                            headers={'User-Agent': 'CrySyS'})
    logger.info(f'GET {response.status_code} with body: {response.text}')
    print(f'The final result:\n\n {response.text}')
