from django.db import connections
from django.db.utils import OperationalError

from django.db import models


# Create your models here.

class ContactManager(models.Manager):

    def create_data(self, request_data):
        self.create(**request_data)
        msg = {'message': 'Success'}
        return msg, 201


class ContactInfo(models.Model):
    name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=11)
    email = models.EmailField(null=True, blank=True)

    objects = ContactManager()

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):

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

        if primary_conn and secondary_conn and replica_conn :
            super(ContactInfo, self).save(using='postgres_db')
            super(ContactInfo, self).save(using='default')
            super(ContactInfo, self).save(using='replica')

        if primary_conn:
            super(ContactInfo, self).save(using='default')
        elif secondary_conn:
            super(ContactInfo, self).save(using='postgres_db')
        elif replica_conn:
            super(ContactInfo, self).save(using='replica')

    def __str__(self):
        return self.name
