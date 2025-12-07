"""
Django app configuration for entities
Required for Django to recognize this as an application
"""

from django.apps import AppConfig


class EntitiesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'entities'
    verbose_name = 'Meal App Entities'
