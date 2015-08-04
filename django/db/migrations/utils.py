from django.apps import apps
from django.db.migrations.autodetector import MigrationAutodetector
from django.db.migrations.loader import MigrationLoader
from django.db.migrations.state import ProjectState


def has_unmigrated_models(loader=None, connection=None):
    """
    :return: A (possibly empty) list of messages,
    if the currently registered models have changes that are not
    yet represented in a migration
    """
    messages = []
    if loader is None:
        loader = MigrationLoader(connection)

    autodetector = MigrationAutodetector(
        loader.project_state(),
        ProjectState.from_apps(apps),
    )
    if autodetector.changes(graph=loader.graph):
        messages.append(
            "  Your models have changes that are not yet reflected "
            "in a migration, and so won't be applied.")
        messages.append(
            "  Run 'manage.py makemigrations' to make new "
            "migrations, and then re-run 'manage.py migrate' to apply them.")
    return messages
