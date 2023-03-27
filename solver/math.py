import socket
import time
import logging

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
