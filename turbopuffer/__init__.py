import os
api_key = os.environ.get('TURBOPUFFER_API_KEY')
api_base_uri = os.environ.get('TURBOPUFFER_API_BASE_URI', 'https://api.turbopuffer.com/v1')

from turbopuffer.version import VERSION
from turbopuffer.namespace import Namespace
from turbopuffer.vectors import VectorColumns, VectorRow