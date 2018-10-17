# -*- coding: utf-8 -*-
# Part of Sailotech. See LICENSE file for full copyright and licensing details.

{
    'name': 'Project - Sprint & Scrum',
    'category': "Project",
    'summary': 'Adds the ability to create Sprints and Scrum teams.',
    'website': 'https://www.sailotech.com/',
    'version': '11.0',
    'license': 'AGPL-3',
    'description': """
        This module allows you to organize your tasks with the Scrum methodology. Using sprints, you can easily plan when your tasks should be done.
        """,
    'author': 'Sailotech Pvt Ltd',
    'depends': ['project',],
    'data': [
        'security/ir.model.access.csv',
        'views/project_view.xml',
        
    ],
    'qweb': [],
    'demo': [
    ],
    'css': [
    ],
    'installable': True,
    'application': False,
}
