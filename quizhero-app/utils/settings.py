"""
Extract heavy logic from project_name/settings.py, manage.py and wsgi.py
"""

from django.conf import settings
from django.utils.module_loading import import_string

def get_project_package(project_dir):
    if (project_dir / "project_name").exists():
        return "project_name"

    return "quizhero_app"


DEFAULT_SETTINGS = {}


def get_configuration(name):
    return getattr(settings, name.upper(), DEFAULT_SETTINGS.get(name))


def get_object_from_configuration(name):
    return import_string(get_configuration(name))
