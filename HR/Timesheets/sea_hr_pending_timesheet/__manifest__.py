
{
    "name": "SEA Pending Timesheet Report",
    "summary": " Employees Pending Timesheets Report Month wise & week wise",
    "version": "11.0.1.0.0",
    "author": "Sailotech Pvt. Ltd.",
    "website": "http://www.sailotech.com",
    "category": "Timesheets",
    "depends": ["project","hr","base","hr_timesheet"],
    "license": "AGPL-3",
    "data": [
        'security/ir.model.access.csv',
        "wizard/pending_timesheet_view.xml",
        "views/pending_view.xml",
        "pending_time_sheet.sql"
        
    ],
    'installable': True,
}
