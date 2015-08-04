from django.apps import apps
from django.db.migrations.autodetector import MigrationAutodetector
from django.db.migrations.loader import MigrationLoader
from django.db.migrations.state import ProjectState


def has_unmigrated_models(loader=None, connection=None):
    """
    Returns True if the currently registered models have changes that are not
    yet represented in a migration
    """
    if loader is None:
        loader = MigrationLoader(connection)

    autodetector = MigrationAutodetector(
        loader.project_state(),
        ProjectState.from_apps(apps),
    )
    return bool(autodetector.changes(graph=loader.graph))


def check_unmigrated_models(loader=None, connection=None, command=None):
    """
    Prints helpful messages for the developer
    if unmigrated models are detected.

    :param command: The Django management Command instance
        which this function is being called from.
    :return: Same as has_unmigrated_models.
    """
    result = has_unmigrated_models(loader, connection)
    if result:
        message1 = (
            "  Your models have changes that are not yet reflected "
            "in a migration, and so won't be applied."
        )
        message2 = (
            "  Run 'manage.py makemigrations' to make new "
            "migrations, and then re-run 'manage.py migrate' to "
            "apply them."
        )
        if hasattr(command, 'stdout') and hasattr(command, 'style'):
            command.stdout.write(command.style.NOTICE(message1))
            command.stdout.write(command.style.NOTICE(message2))
        else:
            print(message1)
            print(message2)
    return result
