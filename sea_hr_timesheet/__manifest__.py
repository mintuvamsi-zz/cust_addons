# -*- coding: utf-8 -*-
# Copyright 2018-19 Sailotech Pvt. Ltd.
#     (www.sailotech.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "SEA Timesheet Aprroval",
    "summary": "Allows to define the week start date for Timesheets at "
               "company level",
    "version": "11.0.1.0.0",
    "author": "Sailotech Pvt. Ltd.",
    "website": "http://www.sailotech.com",
    "category": "Generic",
    "depends": ['mail','project','base'],
    "license": "AGPL-3",
    "data": [
        "wizard/send_manager_view.xml",
        "wizard/manager_approval_view.xml",
        "views/hr_timesheet_sheet_view.xml",
        "views/res_config_settings_view.xml",
    ],
    'installable': True,
}