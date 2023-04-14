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

import socket
import time
import logging
from solution.solver import secrecy

logger = logging.getLogger(__name__)


def solve_equations(s: socket.socket) -> tuple[socket.socket, int]:
    """
    Dialog example:


    Welcome: DASGYJ\n
    I will send you 6 equations!\n
    Send me the solutions!\n
    01. 96589 - 91606 =
    :param s:
    :return:
    """
    time.sleep(0.3)
    message = str(s.recv(1024), 'utf-8')
    logger.debug(f'Received: {message}')
    lines = message.splitlines()

    if len(lines) != 4:
        logger.error("Received incorrect data")
        s.close()
        raise "Not valid"

    # oof
    n_equation = int(lines[1][16:].split(' ')[0])
    logger.info(f'There will be {n_equation} equations')
    last_result = 0
    last_result = __solve(lines[3][4:-1].strip())
    s.send(bytes(str(last_result), 'utf-8'))

    for _ in range(1, n_equation):
        message = str(s.recv(1024), 'utf-8')
        logger.debug(f'Received: {message}')
        last_result = __solve(message[4:].strip())
        s.send(bytes(str(last_result), 'utf-8'))

    return s, last_result


def __solve(equation: str) -> int:
    """
    Solves an equation
    :param equation: received equation
    :return: returns the result of the equation
    """
    logger.info(f'Now solving equation: {equation}')
    equation = equation[:-2]
    logger.debug(f'Stripped equation: {equation}')
    problems = equation.split(' ')
    result = 0
    negate = False
    for problem in problems:
        if problem == '+':
            negate = False
            continue
        elif problem == '-':
            negate = True
            continue

        if negate:
            result = result - int(problem)
        else:
            result = result + int(problem)

    logger.debug(f'Calculated result: {result}')
    return result


def roll_dem_dice(base_text: str) -> tuple[str, str]:
    """

    :param last_result:
    :return:
    """
    i = 0
    while True:
        text = f'{base_text}{i:x}'
        _hash = secrecy.encrypt_str(text)
        if _hash.startswith('0000'):
            logger.info(f'Found str: {text} with hash: {_hash}')
            return text, _hash

        if i > 1_048_575:
            break
        i = i + 1

    raise 'No string found'
