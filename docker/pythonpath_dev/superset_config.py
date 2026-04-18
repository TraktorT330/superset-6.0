# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
# This file is included in the final Docker image and SHOULD be overridden when
# deploying the image to prod. Settings configured here are intended for use in local
# development environments. Also note that superset_config_docker.py is imported
# as a final step as a means to override "defaults" configured here
#
import logging
import os
import sys

from celery.schedules import crontab
from flask_caching.backends.filesystemcache import FileSystemCache

logger = logging.getLogger()

DATABASE_DIALECT = os.getenv("DATABASE_DIALECT")
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_PORT = os.getenv("DATABASE_PORT")
DATABASE_DB = os.getenv("DATABASE_DB")

EXAMPLES_USER = os.getenv("EXAMPLES_USER")
EXAMPLES_PASSWORD = os.getenv("EXAMPLES_PASSWORD")
EXAMPLES_HOST = os.getenv("EXAMPLES_HOST")
EXAMPLES_PORT = os.getenv("EXAMPLES_PORT")
EXAMPLES_DB = os.getenv("EXAMPLES_DB")

# The SQLAlchemy connection string.
SQLALCHEMY_DATABASE_URI = (
    f"{DATABASE_DIALECT}://"
    f"{DATABASE_USER}:{DATABASE_PASSWORD}@"
    f"{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_DB}"
)

SQLALCHEMY_EXAMPLES_URI = (
    f"{DATABASE_DIALECT}://"
    f"{EXAMPLES_USER}:{EXAMPLES_PASSWORD}@"
    f"{EXAMPLES_HOST}:{EXAMPLES_PORT}/{EXAMPLES_DB}"
)

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")
REDIS_CELERY_DB = os.getenv("REDIS_CELERY_DB", "0")
REDIS_RESULTS_DB = os.getenv("REDIS_RESULTS_DB", "1")

RESULTS_BACKEND = FileSystemCache("/app/superset_home/sqllab")

CACHE_CONFIG = {
    "CACHE_TYPE": "RedisCache",
    "CACHE_DEFAULT_TIMEOUT": 900,
    "CACHE_KEY_PREFIX": "superset_",
    "CACHE_REDIS_HOST": REDIS_HOST,
    "CACHE_REDIS_PORT": REDIS_PORT,
    "CACHE_REDIS_DB": REDIS_RESULTS_DB,
}
DATA_CACHE_CONFIG = CACHE_CONFIG
THUMBNAIL_CACHE_CONFIG = {
    "CACHE_TYPE": "RedisCache",
    "CACHE_DEFAULT_TIMEOUT": 60 * 60,
    "CACHE_KEY_PREFIX": "development_superset_thumbs_",
    "CACHE_REDIS_HOST": REDIS_HOST,
    "CACHE_REDIS_PORT": REDIS_PORT,
    "CACHE_REDIS_DB": REDIS_RESULTS_DB,
}


class CeleryConfig:
    broker_url = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_CELERY_DB}"
    imports = (
        "superset.sql_lab",
        "superset.tasks.scheduler",
        "superset.tasks.thumbnails",
        "superset.tasks.cache",
    )
    result_backend = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_RESULTS_DB}"
    worker_prefetch_multiplier = 1
    task_acks_late = False
    beat_schedule = {
        "reports.scheduler": {
            "task": "reports.scheduler",
            "schedule": crontab(minute="*", hour="*"),
        },
        "reports.prune_log": {
            "task": "reports.prune_log",
            "schedule": crontab(minute=10, hour=0),
        },
    }


CELERY_CONFIG = CeleryConfig

CUSTOM_COLOR_SCHEME = {
    "label": "My Custom Scheme",
    "colors": [
        "#FF5733",
        "#33FF57",
        "#3357FF",
        "#FF33A1",
        "#FF8C33",
        "#33FFF3",
        "#FF3380",
        "#80FF33",
        "#3380FF",
        "#FFDB33",
        "#DB33FF",
        "#33FFDB",
        "#FF335B",
    ],
}
EXTRA_CATEGORICAL_COLOR_SCHEMES = [CUSTOM_COLOR_SCHEME]

FEATURE_FLAGS = {
    "DRUID_JOINS": False,
    "DYNAMIC_PLUGINS": False,
    "ENABLE_TEMPLATE_PROCESSING": True,
    "ENABLE_JAVASCRIPT_CONTROLS": False,
    "PRESTO_EXPAND_DATA": False,
    "THUMBNAILS": True,
    "ENABLE_DASHBOARD_SCREENSHOT_ENDPOINTS": True,
    "ENABLE_DASHBOARD_DOWNLOAD_WEBDRIVER_SCREENSHOT": True,
    "TAGGING_SYSTEM": True,
    "SQLLAB_BACKEND_PERSISTENCE": True,
    "LISTVIEWS_DEFAULT_CARD_VIEW": False,
    "ESCAPE_MARKDOWN_HTML": False,
    "DASHBOARD_VIRTUALIZATION": True,
    "GLOBAL_ASYNC_QUERIES": False,
    "EMBEDDED_SUPERSET": True,
    "ALERT_REPORTS": True,
    "ALERT_REPORT_TABS": True,
    "ALERT_REPORT_SLACK_V2": True,
    "DASHBOARD_RBAC": True,
    "ENABLE_ADVANCED_DATA_TYPES": True,
    "ALERTS_ATTACH_REPORTS": True,
    "ALLOW_FULL_CSV_EXPORT": True,
    "ALLOW_ADHOC_SUBQUERY": True,
    "USE_ANALOGOUS_COLORS": True,
    "RLS_IN_SQLLAB": False,
    "OPTIMIZE_SQL": False,
    "IMPERSONATE_WITH_EMAIL_PREFIX": False,
    "CACHE_IMPERSONATION": False,
    "CACHE_QUERY_BY_USER": False,
    "EMBEDDABLE_CHARTS": True,
    "DRILL_TO_DETAIL": True,
    "DRILL_BY": True,
    "DATAPANEL_CLOSED_BY_DEFAULT": False,
    "HORIZONTAL_FILTER_BAR": True,
    "ESTIMATE_QUERY_COST": True,
    "SSH_TUNNELING": False,
    "AVOID_COLORS_COLLISION": True,
    "MENU_HIDE_USER_INFO": False,
    "ENABLE_SUPERSET_META_DB": True,
    "PLAYWRIGHT_REPORTS_AND_THUMBNAILS": True,
    "CHART_PLUGINS_EXPERIMENTAL": True,
    "SQLLAB_FORCE_RUN_ASYNC": False,
    "ENABLE_FACTORY_RESET_COMMAND": False,
    "SLACK_ENABLE_AVATARS": True,
    "DATE_FORMAT_IN_EMAIL_SUBJECT": False,
}

GUEST_ROLE_NAME = "Public"
SQLLAB_PAYLOAD_MAX_MB = 50000

HTML_SANITIZATION = False

WTF_CSRF_ENABLED = False
WTF_CSRF_EXEMPT_LIST = [
    r"^/api/v1/security/guest_token/?$",
]

ENABLE_CORS = True
CORS_OPTIONS = {
    "supports_credentials": True,
    "allow_headers": ["*"],
    "resources": ["*"],
    "origins": ["*"],
}

TALISMAN_ENABLED = False

SUPERSET_META_DB_LIMIT = None
ALERT_REPORTS_NOTIFICATION_DRY_RUN = False

WEBDRIVER_BASEURL = (
    f"http://superset:8088{os.environ.get('SUPERSET_APP_ROOT', '/')}"
)
# The base URL for the email report hyperlinks.
WEBDRIVER_BASEURL_USER_FRIENDLY = (
    f"http://localhost:8888/{os.environ.get('SUPERSET_APP_ROOT', '/')}/"
)
SQLLAB_CTAS_NO_LIMIT = True

D3_FORMAT = {
    "decimal": ".",
    "thousands": " ",
    "grouping": [3],
    "currency": ["$", ""],
}

# Row and payload limits aligned with the Superset 5 setup.
ROW_LIMIT = 5_000_000
SQL_MAX_ROW = 500_000
DISPLAY_MAX_ROW = 100_000_000
SAMPLES_ROW_LIMIT = 100_000
NATIVE_FILTER_DEFAULT_ROW_LIMIT = 10
FILTER_SELECT_ROW_LIMIT = 1000
SUPERSET_DASHBOARD_POSITION_DATA_LIMIT = 655_350

DISPLAY_TIMEZONE = "Asia/Yekaterinburg"
SQLALCHEMY_TRACK_MODIFICATIONS = True

DECKGL_BASE_MAP = [
    ["https://tile.openstreetmap.org/{z}/{x}/{y}.png", "Streets (OSM)"],
    ["https://tile.osm.ch/osm-swiss-style/{z}/{x}/{y}.png", "Topography (OSM)"],
    ["mapbox://styles/mapbox/streets-v9", "Streets"],
    ["mapbox://styles/mapbox/dark-v9", "Dark"],
    ["mapbox://styles/mapbox/light-v9", "Light"],
    ["mapbox://styles/mapbox/satellite-streets-v9", "Satellite Streets"],
    ["mapbox://styles/mapbox/satellite-v9", "Satellite"],
    ["mapbox://styles/mapbox/outdoors-v9", "Outdoors"],
]

TIME_GRAIN_ADDONS = {
    "PT2S": "2 second",
    "PT15S": "15 second",
}

TIME_GRAIN_ADDON_EXPRESSIONS = {
    "clickhousedb": {
        "PT2S": "toDateTime(intDiv(toUInt32(toDateTime({col})), 2) * 2)",
        "PT15S": "toDateTime(intDiv(toUInt32(toDateTime({col})), 15) * 15)",
    },
    "postgresql": {
        "PT2S": "to_timestamp(floor(extract(epoch FROM {col}) / 2) * 2)",
        "PT15S": "to_timestamp(floor(extract(epoch FROM {col}) / 15) * 15)",
    },
}


def format_user_greeting(username="Guest"):
    """Return a simple greeting for Jinja macro usage."""
    if not username:
        username = "Guest"
    return f"Привет, {username}! Добро пожаловать в Superset."


def generate_where_clause(column, value):
    """Generate a simple WHERE clause for Jinja macro usage."""
    logger.warning(
        "Using unsafe generate_where_clause/custom_where macro in Jinja context."
    )
    return f"{column} = '{value}'"


def my_crazy_macro(x):
    """Multiply a numeric value by 2 for Jinja macro usage."""
    try:
        return int(x) * 2
    except (ValueError, TypeError):
        return "Ошибка: Ожидалось число"


current_jinja_addons = globals().get("JINJA_CONTEXT_ADDONS", {})
current_jinja_addons.update(
    {
        "format_user_greeting": format_user_greeting,
        "custom_where": generate_where_clause,
        "my_crazy_macro": my_crazy_macro,
    }
)
JINJA_CONTEXT_ADDONS = current_jinja_addons

log_level_text = os.getenv("SUPERSET_LOG_LEVEL", "INFO")
LOG_LEVEL = getattr(logging, log_level_text.upper(), logging.INFO)

if os.getenv("CYPRESS_CONFIG") == "true":
    # When running the service as a cypress backend, we need to import the config
    # located @ tests/integration_tests/superset_test_config.py
    base_dir = os.path.dirname(__file__)
    module_folder = os.path.abspath(
        os.path.join(base_dir, "../../tests/integration_tests/")
    )
    sys.path.insert(0, module_folder)
    from superset_test_config import *  # noqa

    sys.path.pop(0)

#
# Optionally import superset_config_docker.py (which will have been included on
# the PYTHONPATH) in order to allow for local settings to be overridden.
# Values from this local override file replace the base settings above, including
# options like EMAIL_NOTIFICATIONS, SMTP_*, SECRET_KEY, and other env-specific
# Docker settings.
#
try:
    import superset_config_docker
    from superset_config_docker import *  # noqa: F403

    logger.info(
        f"Loaded your Docker configuration at [{superset_config_docker.__file__}]"
    )
except ImportError:
    logger.info("Using default Docker config...")
