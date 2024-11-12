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

# class HREIDTracker(models.Model):
#     _name = 'hr.eid.tracker'
#     _description = 'Employee ID Number Assignment'
    # _rec_name = 'employee_id' 

    # active = fields.Boolean('Active', store=True, default=True)
    # # eid = fields.Char('Employee ID (Dupli)', store=True)
    # employee_id = fields.Char('Employee ID', store=True)

    # @api.constrains('employee_id')
    # def _check_duplicate(self):
    #     for record in self:
    #         # Check if there are other records with the same employee_id
    #         if record.employee_id:
    #             duplicate_records = self.search([('employee_id', '=', record.employee_id), ('id', '!=', record.id)])
    #             if duplicate_records:
    #                 raise ValidationError('Employee Id already exists.')
    
    # first_name = fields.Char('First Name', store=True, readonly=False)
    # last_name = fields.Char('Last Name', store=True, readonly=False)
    # account = fields.Many2one('accounts', string='Account', store=True, readonly=False)
    # position = fields.Char('Position', store=True, readonly=False)
    # start_date = fields.Date('Start Date', store=True, readonly=False)
    # payroll_credential_status = fields.Char('Payroll Credential Status', store=True, readonly=False)
    # complete_name = fields.Char('Complete Name', store=True, compute='_compute_complete_name')
   
    # @api.depends('first_name', 'last_name')
    # def _compute_complete_name(self):
    #     for record in self:
    #         if record.first_name and record.last_name:
    #             record.complete_name = record.first_name + ' ' + record.last_name
    #         else:
    #             record.complete_name = False

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
    #                 if not record.first_name:
    #                     record.first_name = auto_populate_record.first_name
    #                 if not record.last_name:
    #                     record.last_name = auto_populate_record.last_name
    #                 if not record.account:
    #                     record.account = auto_populate_record.account
    #                 if not record.position:
    #                     record.position = auto_populate_record.position
    #                 if not record.start_date:
    #                     record.start_date = auto_populate_record.official_start_date

    #                 # Store the initial values for future comparison
    #                 record.auto_populate_function = {
    #                     'first_name': auto_populate_record.first_name,
    #                     'last_name': auto_populate_record.last_name,
    #                     'account': auto_populate_record.account,
    #                     'position': auto_populate_record.position,
    #                     'start_date': auto_populate_record.official_start_date,
    #                 }
    #             else:
    #                 pass
                