from core.permit.client import CurlClient
from core.permit.licenses import get_device_data
from core.exceptions import *
from core.response import *
from core.logger import get_logger, logger, log_exception, handle_exception