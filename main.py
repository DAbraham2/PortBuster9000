# This is a sample Python script.
import logging
import time

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import buster.port as portbuster
from solver import math, secrecy


def main():
    addr = '152.66.249.144'
    portbuster.init_bust(ip_addr=addr, delay=500, timeout=400)
    soc = portbuster.connect(addr)
    soc, res = math.solve_equations(soc)
    time.sleep(0.3)
    logging.debug(str(soc.recv(1024), 'utf-8'))
    val = secrecy.encrypt(res)
    soc.send(bytes(val, 'utf-8'))
    time.sleep(0.3)
    logging.debug(str(soc.recv(1024), 'utf-8'))
    soc.close()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
