import logging

from Cryptodome.Hash import SHA1

logger = logging.getLogger(__name__)


def encrypt(last_result: int) -> str:
    """

    :param last_result:
    :return:
    """
    h = SHA1.new(bytes('DASGYJ'+str(last_result), 'utf-8'))
    val = h.hexdigest().lower()
    logger.info(f'Calculated hash: {val}')
    return val

