

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

import logging
import time

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
