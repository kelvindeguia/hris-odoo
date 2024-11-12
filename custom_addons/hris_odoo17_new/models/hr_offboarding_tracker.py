# import logging
# import pytz
# import threading
# from collections import OrderedDict, defaultdict
# from datetime import date, datetime, timedelta
# from psycopg2 import sql

# from odoo import api, fields, models, tools, SUPERUSER_ID
# from odoo.exceptions import UserError, AccessError
# from odoo.osv import expression
# from odoo.tools.translate import _
# from odoo.tools import date_utils, email_re, email_split, is_html_empty, groupby
# from odoo.tools.misc import get_lang
# from random import randint
# from odoo.exceptions import ValidationError

# class HR_OffBoarding_Tracker(models.Model):
#     _name = 'hr.offboarding.tracker'
#     _description = 'HR Offboarding Tracker'
    # _rec_name = 'employee_id'

    # active = fields.Boolean('Active', store=True, default=True)
    # employee_id = fields.Char('Employee ID', store=True)
    # # Employee ID VALIDATION ERROR
    # @api.constrains('employee_id')
    # def _check_duplicate(self):
    #     for record in self:
    #         # Check if there are other records with the same employee_id
    #         if record.employee_id:
    #             duplicate_records = self.search([('employee_id', '=', record.employee_id), ('id', '!=', record.id)])
    #             if duplicate_records:
    #                 raise ValidationError('Employee Id already exists.')    
                  
    # employee_name = fields.Char('Employee Name', store=True, readonly=False)
    # account = fields.Many2one('accounts', string='Account', store=True, readonly=False)
    # hire_date = fields.Date('Hire Date', store=True, readonly=False)
    # last_working_date = fields.Char('Last Working Date', store=True)
    # seperation_date = fields.Date('Seperation Date', store=True)
    # c_company = fields.Selection([('isupport_worldwide', 'iSupport Worldwide'), ('iswerk', 'ISWerk')],'Company', store=True, readonly=False)
    # overall_clearance_status = fields.Char('Overall Clearance Status', store=True)
    # hr_remarks = fields.Text('HR Remarks', store=True)
    # disabling_of_it_access = fields.Char('Disabling of IT Access', store=True)
    # odoo_access_disabling = fields.Char('Odoo Access Disabling', store=True)
    # assets_pullout_status = fields.Char('Asset Pull Out Status(Assets Deployed Onsite)', store=True)
    # it_assets_returned = fields.Char('IT Assets Returned?', store=True)
    # pending_it_assets_to_be_returned = fields.Char('Pending IT Assets to be Returned', store=True)
    # it_clearance_status = fields.Char('IT Clearance Status', store=True)
    # it_remarks = fields.Text('IT Remarks', store=True)
    # locker_facilities = fields.Char('Locker Key', store=True)
    # pedestal_key = fields.Char('Pedestal Key', store=True)
    # accesories = fields.Char('Accessories', store=True)
    # facilities_clearance_status = fields.Char('Facilities Clearance Status', store=True)
    # facilities_remarks = fields.Text('Facilities Remarks', store=True)
    # created = fields.Datetime('Created', store=True)
    # item_type = fields.Char('Item Type', store=True)
    # path = fields.Char('Path', store=True)

    # # USED FOR THE AUTO-POPULATE FUNCTION
    # auto_populate_function = fields.Char(string='Original Values')
    # #  # Define compute method to auto-populate employee_name based on employee_id
    # @api.onchange('employee_id')

    # def _compute_auto_populate(self):
    #     for record in self:
    #         if record.employee_id:
    #             auto_populate_record = self.env['hr.new.hire.trackers'].search([('employee_id', '=', record.employee_id)], limit=1)
    #             if auto_populate_record:
    #                 # Assigning values only if the fields are empty or haven't been modified
    #                 if not record.employee_name:
    #                     record.employee_name = auto_populate_record.complete_name
    #                 if not record.account:
    #                     record.account = auto_populate_record.account
    #                 if not record.hire_date:
    #                     record.hire_date = auto_populate_record.hire_date
    #                 if not record.c_company:
    #                     record.c_company = auto_populate_record.c_company

    #                 # Store the initial values for future comparison
    #                 record.auto_populate_function = {
    #                     'employee_name': auto_populate_record.complete_name,
    #                     'account': auto_populate_record.account,
    #                     'hire_date': auto_populate_record.hire_date,
    #                     'c_company': auto_populate_record.c_company,
    #                 }
    #             else:
    #                 pass

