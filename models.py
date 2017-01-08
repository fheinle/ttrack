#!/usr/bin/env python3

from peewee import Model, SqliteDatabase
from peewee import IntegerField, CharField, BooleanField
from peewee import DateTimeField, ForeignKeyField

database = SqliteDatabase('db.sqlite')

class ModelBase(Model):
    class Meta:
        database = database

class Project(ModelBase):
    projectId = CharField(unique=True, primary_key=True) # comes from TimeSheet
    name = CharField()
    employer = CharField(null=True)
    salary = IntegerField() # cents
    location = CharField(null=True)

    def __repr__(self):
        return '<Project ({})>'.format(self.name)

class Task(ModelBase):
    taskId = CharField(unique=True, primary_key=True) # comes from timesheet
    description = CharField(null=True)
    location = CharField(null=True)
    startDate = DateTimeField()
    endDate = DateTimeField()
    feeling = IntegerField(null=True)
    projectId = ForeignKeyField(Project)
    billable = BooleanField()
    paid = BooleanField()

    def __repr__(self):
        return '<Task ({})>'.format(self.description)

def create_tables():
    database.connect()
    database.create_tables([Project, Task])
