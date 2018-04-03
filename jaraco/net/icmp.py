import warnings

from jaraco.email.smtp import * # noqa

warnings.warn("Use jaraco.email package", DeprecationWarning)
