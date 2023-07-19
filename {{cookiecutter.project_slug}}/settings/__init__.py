import os

from .common import *

env = os.environ.get("environment")

if env == "production":
    from .prod import *
else:
    from .dev import *
