__version__ = '0.11.0'

from .process_flights import AirspaceHandler
from .utils import config, DataConfig

import logging
logging.getLogger(__name__).addHandler(logging.NullHandler())