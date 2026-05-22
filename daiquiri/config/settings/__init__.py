# Inclui settings do pacote django-daiquiri
from daiquiri.auth.settings import *
from daiquiri.conesearch.settings import *
from daiquiri.core.settings.daiquiri import *
from daiquiri.core.settings.django import *
from daiquiri.core.settings.logging import *
from daiquiri.cutout.settings import *
from daiquiri.datalink.settings import *
from daiquiri.files.settings import *
from daiquiri.jobs.settings import *
from daiquiri.metadata.settings import *
from daiquiri.oai.settings import *
from daiquiri.query.settings import *
from daiquiri.registry.settings import *
from daiquiri.serve.settings import *
from daiquiri.stats.settings import *
from daiquiri.tap.settings import *

# Sobrescreve com base.py (versionado no git)
try:
    from .base import *
except ImportError:
    pass

# Sobrescreve com local.py (não versionado)
try:
    from .local import *
except ImportError:
    pass

try:
    from .logging import *
except ImportError:
    pass
