import os

from settings.common import *

if os.environ.get("DEV"):
    from settings.development import *