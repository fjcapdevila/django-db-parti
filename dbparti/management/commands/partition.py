from dbparti.models import Partitionable
from django.db.models import get_models, connection
from django.core.management.base import AppCommand


class Command(AppCommand):
    help = 'Configures the database for partitioned models'

    def handle_app(self, app, **options):
        """Configures all needed database stuff depending on the backend used"""
        names = []

        for model in get_models(app):
            if issubclass(model, Partitionable):
                names.append(model.__name__)

                db = getattr(__import__('dbparti.backends.' + connection.vendor,
                    fromlist=[connection.vendor.capitalize()]), connection.vendor.capitalize())(
                        model._meta.db_table, model._meta.partition_column)

                db.init_partition(model._meta.partition_range)

        if not names:
            self.stderr.write('Unable to find any partitionable models in an app: ' + app.__name__.split('.')[0])
        else:
            self.stdout.write('Successfully (re)configured the database for the following models: ' + ', '.join(names))
