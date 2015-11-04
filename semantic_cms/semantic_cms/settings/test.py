"""
Test settings and globals for local running of
the test suite.

You can run the tests (from the root Django directory) with these settings like this:
    django-admin.py test --settings=semantic_cms.settings.test --verbosity=2
The verbosity settings is optional, running without (default value is '1')
is usually sufficient as you don't need to see successful tests, necessarily.
"""

from .base import *

### Test Settings ###
# TEST_RUNNER = "discover_runner.DiscoverRunner"
TEST_DISCOVER_TOP_LEVEL = BASE_DIR
TEST_DISCOVER_ROOT = BASE_DIR
TEST_DISCOVER_PATTERN = "test_*"

### Using In-Memory Test Database ###
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
        "USER": "",
        "PASSWORD": "",
        "HOST": "",
        "PORT": "",
    },
}
