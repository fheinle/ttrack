#!/usr/bin/env python3

""" read timesheet data file into sqlite """

from sys import argv

from lxml.objectify import fromstring
from peewee import IntegrityError
from iso8601 import parse_date

import models

def create_instance(model, **kwargs):
    """Create a new instance of model only if it's not already there"""
    try:
        with models.database.transaction():
            model.create(**kwargs)
    except IntegrityError:
        pass
    return True

def input_file(input_fname):
    """read an XML backup file from timesheet

    returns nested dictionaries with projects, tasks, etc"""

    with open(input_fname, 'r') as ts_file:
        ts_data = fromstring(ts_file.read())
        for xml_project in ts_data.projects.getchildren():
            create_instance(models.Project,
                            projectId=str(xml_project.projectId),
                            name=str(xml_project.name),
                            employer=str(xml_project.employer),
                            salary=int(xml_project.salary * 100),
                            location=str(xml_project.location),
                           )
        for xml_task in ts_data.tasks.getchildren():
            create_instance(models.Task,
                            taskId=str(xml_task.taskId),
                            description=str(xml_task.description),
                            loction=str(xml_task.location),
                            startDate=parse_date(str(xml_task.startDate)),
                            endDate=parse_date(str(xml_task.endDate)),
                            feeling=int(xml_task.feeling),
                            projectId=str(xml_task.projectId),
                            billable=bool(xml_task.billable),
                            paid=bool(xml_task.paid),
                           )

def main(argv):
    """ran from command line"""
    if argv[1] == '-i':
        models.create_tables()
    else:
        input_file(argv[1])

if __name__ == '__main__':
    main(argv)
