from django.apps import apps
from django.db.migrations.autodetector import MigrationAutodetector
from django.db.migrations.loader import MigrationLoader
from django.db.migrations.state import ProjectState


import time


def timethis(func):
    """
    Very basic version since we can't easily use Python's timeit.
    Feel free to improve :)
    """
    def wrap(*args, **kwargs):
        start = time.time()
        try:
            result = func(*args, **kwargs)
            return result
        finally:
            msg = '%s - Took %.3f seconds' % (
                func.__name__, time.time() - start
            )
            print(msg)

    return wrap


@timethis
def has_unmigrated_models(loader=None, connection=None):
    """
    Returns True if the currently registered models have changes that are not
    yet represented in a migration
    """
    if loader is None:
        loader = MigrationLoader(connection)

    autodetector = MigrationAutodetector(loader.project_state(), ProjectState.from_apps(apps))
    return bool(autodetector.changes(graph=loader.graph))
