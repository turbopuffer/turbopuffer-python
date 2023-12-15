import os
api_key = os.environ.get('TURBOPUFFER_API_KEY')
api_base_url = os.environ.get('TURBOPUFFER_API_BASE_URL', 'https://api.turbopuffer.com/v1')

from turbopuffer.version import VERSION
from turbopuffer.namespace import Namespace
from turbopuffer.vectors import VectorColumns, VectorRow
from turbopuffer.query import VectorQuery
from turbopuffer.error import TurbopufferError, AuthenticationError, APIError