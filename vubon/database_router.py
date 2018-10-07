import random

from django.db import connections
from django.db.utils import OperationalError


class PrimaryReplicaRouter:
    """

    """
    def db_for_read(self, model, **hints):
        """
        Reads go to a randomly-chosen replica.
        """
        primary_db = connections['default']
        secondary_db = connections['postgres_db']
        replica_db = connections['replica']

        try:
            primary_conn = primary_db.cursor()
        except OperationalError:
            primary_conn = False
        try:
            secondary_conn = secondary_db.cursor()
        except OperationalError:
            secondary_conn = False

        try:
            replica_conn = replica_db.cursor()
        except OperationalError:
            replica_conn = False

        # if both DBs connection is okay, then read data randomly
        if primary_conn and secondary_conn and replica_conn:
            return random.choice(['default', 'postgres_db', 'replica'])

        if primary_conn:
            return 'default'
        elif secondary_conn:
            return 'postgres_db'
        elif replica_conn:
            return 'replica'

    def db_for_write(self, model, **hints):
        """
        Writes always go to primary.
        """
        print(model.__dict__)
        # return 'default'
        db_list = ['default', 'postgres_db']
        for db in db_list:
            return db

    def allow_relation(self, obj1, obj2, **hints):
        """
        Relations between objects are allowed if both objects are
        in the primary/replica pool.
        """
        db_list = ('default', 'postgres_db',)
        if obj1._state.db in db_list and obj2._state.db in db_list:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        All non-auth models end up in this pool.
        """
        return True
