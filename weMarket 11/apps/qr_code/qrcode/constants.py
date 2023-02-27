from datetime import datetime

from qrcode import ERROR_CORRECT_L, ERROR_CORRECT_M, ERROR_CORRECT_Q, ERROR_CORRECT_H

from qr_code.qrcode.image import SVG_FORMAT_NAME

QR_CODE_GENERATION_VERSION_DATE = datetime(year=2018, month=3, day=15, hour=0)
ALLOWS_EXTERNAL_REQUESTS_FOR_REGISTERED_USER = 'ALLOWS_EXTERNAL_REQUESTS_FOR_REGISTERED_USER'
SIZE_DICT = {'t': 6, 's': 12, 'm': 18, 'l': 30, 'h': 48}
ERROR_CORRECTION_DICT = {'L': ERROR_CORRECT_L, 'M': ERROR_CORRECT_M, 'Q': ERROR_CORRECT_Q, 'H': ERROR_CORRECT_H}
DEFAULT_MODULE_SIZE = 'M'
DEFAULT_BORDER_SIZE = 4
DEFAULT_VERSION = None
DEFAULT_IMAGE_FORMAT = SVG_FORMAT_NAME
DEFAULT_CACHE_ENABLED = True
DEFAULT_ERROR_CORRECTION = 'M'