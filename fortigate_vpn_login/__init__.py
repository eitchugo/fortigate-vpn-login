# -*- coding: utf-8 -*-
"""
    fortigate_vpn_login
    ~~~~~~~~~~~~~~~~~~

    Uses openconnect to connect to Fortinet VPNs, with extra features
"""
import logging
import os

__version__ = '0.5'

__author__ = 'Hugo Cisneiros'
__author_email__ = 'hugo.cisneiros@gmail.com'
__maintainer__ = 'Hugo Cisneiros'
__maintainer_email__ = 'hugo.cisneiros@gmail.com'
__description__ = 'Uses openconnect to connect to Fortinet VPNs, with extra features'
__url__ = 'https://github.com/eitchugo/fortigate-vpn-login'
__license__ = 'GPL3'

__credits__ = {
    'Hugo Cisneiros': 'hugo.cisneiros@ifood.com.br',
    'Alexandre Zia': 'alexandre.zia@ifood.com.br'
}

# logging setup
logging.basicConfig(
  # format='[%(asctime)s] [%(levelname)s] %(message)s'
  format='[%(asctime)s] [%(levelname)s] [%(name)s:%(filename)s:%(lineno)s: %(funcName)s()] %(message)s'
)
logging.getLogger().setLevel(os.getenv("LOG_LEVEL", "FATAL"))
logger = logging.getLogger(__name__)
