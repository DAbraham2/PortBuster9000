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
import downloader
import taskSolutions


def main():
    addr = '152.66.249.144'
    portbuster.init_bust(ip_addr=addr, delay=500, timeout=400)
    soc = portbuster.connect(addr)

    soc, res = math.solve_equations(soc)

    soc = taskSolutions.task_EncryptHash(soc)

    soc = taskSolutions.task_SolveExtend(soc)

    # text = math.roll_dem_dice(res)
    # soc.send(bytes(text, 'utf-8'))
    time.sleep(0.3)
    rec = str(soc.recv(1024), 'utf-8')
    logging.info(f'Response for hash: {rec}')
    if rec.startswith('Correct') is False:
        soc.close()
        exit(2)

    taskSolutions.task_navigate_web(soc)
    soc.close()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
