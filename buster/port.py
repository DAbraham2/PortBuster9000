import socket
import time

import select

"""Predefined by the specification"""
__PORT_LIST = [1337, 2674, 4011]


def init_bust(ip_addr: str, delay: int, timeout: int) -> None:
    """
    Initiates a port busting mechanism.

    Clears the first task of the homework.
    :param ip_addr: ip address of the desired server.
    :param delay:
    :param timeout:
    :return: none
    """
    print("Knock knock")
    for port in __PORT_LIST:
        print(f'hitting {ip_addr} on port {port}')
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setblocking(False)
            sock.connect_ex((ip_addr, port))
            select.select([sock], [sock], [sock], timeout / 1000)
            sock.close()

        time.sleep(delay / 1000)

    print("Who's there?")


def connect(ip_addr: str) -> socket.socket:
    """
    Connects to the server on main port
    :param ip_addr:
    :return:
    """

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # s.setblocking(False)
    s.connect((ip_addr, 8888))
    # s.sendall(bytes("DASGYJ", 'utf-8'))
    rec = str(s.recv(1024), 'utf-8')
    rec = rec.strip()
    print(f'Received: {rec}')

    if rec == "Give me your neptun code:":
        print("What a gentleman!")
        s.sendall(bytes("DASGYJ", 'utf-8'))

    return s
