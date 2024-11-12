import logging
import pytz
import threading
from collections import OrderedDict, defaultdict
from datetime import date, datetime, timedelta
from psycopg2 import sql

from odoo import api, fields, models, tools, SUPERUSER_ID
from odoo.exceptions import UserError, AccessError
from odoo.osv import expression
from odoo.tools.translate import _
from odoo.tools import date_utils, email_re, email_split, is_html_empty, groupby
from odoo.tools.misc import get_lang
from random import randint
from odoo.exceptions import ValidationError


class HR_Performance_Review_Tracker(models.Model):
    _name = 'hr.performance.review.tracker'
    _description = 'HR Performance Review Tracker'
    _rec_name = 'employee_number'

    active = fields.Boolean('Active', store=True, index=True, default=True)

    employee_number = fields.Char('Employee Number', store=True, index=True)
    # Employee ID VALIDATION ERROR
    @api.constrains('employee_number')
    def _check_duplicate(self):
        for record in self:
            # Check if there are other records with the same employee_id
            if record.employee_number:
                duplicate_records = self.search([('employee_number', '=', record.employee_number), ('id', '!=', record.id)])
                if duplicate_records:
                    raise ValidationError('Employee Number already exists.')  
                
    complete_name = fields.Char('Complete Name', store=True, index=True, readonly=False)
    hire_date = fields.Date('Hire Date', store=True, index=True, readonly=False)
    c_employment_status = fields.Selection([('', ''),('probationary', 'PROBATIONARY'), ('regular', 'REGULAR'), ('project_based', 'PROJECT-BASED'), ('inactive', 'INACTIVE')],'Employment Status', store=True, index=True, readonly=False)
    # entity = fields.Char('Entity', store=True, index=True, readonly=False)
    c_entity = fields.Selection([('isupport_worldwide', 'iSupport Worldwide'), ('iswerk', 'ISWerk')],'Entity', store=True, index=True, readonly=False)
    department = fields.Selection([('', ''),('operations', 'OPERATIONS'),('support', 'SUPPORT')],'Department', store=True, index=True)
    account = fields.Many2one('accounts', string='Account', store=True, index=True, readonly=False)
    position = fields.Char('Position', store=True, index=True, readonly=False)
    email_address = fields.Char('Email Address', store=True, index=True, readonly=False)

    # Performance Review POC
    performance_review_poc_name = fields.Char('Performance Review POC Name', store=True, index=True)
    performance_review_poc_email_address = fields.Char('Performance Review POC Email Address', store=True, index=True)

    # Performance Review
    comments = fields.Text('Comments', store=True, index=True)

    third_month_review_date = fields.Date('3rd Month Review Date', store=True, index=True)
    third_month_review_accomplished_date = fields.Date('3rd Month Review Accomplished Date', store=True, index=True)

    fifth_month_review_date = fields.Date('5th Month Review Date', store=True, index=True)
    fifth_month_review_accomplished_date = fields.Date('5th Month Review Accomplished Date', store=True, index=True)

    twentyfour_annual_review_date = fields.Date('2024 Annual Review Date', store=True, index=True)
    twentyfour_annual_review_accomplished_date = fields.Date('2024 Annual Review Accomplished Date', store=True, index=True)

    twentyfive_annual_review_date = fields.Date('2025 Annual Review Date', store=True, index=True)
    twentyfive_annual_review_accomplished_date = fields.Date('2025 Annual Review Accomplished Date', store=True, index=True)

    # USED FOR THE AUTO-POPULATE FUNCTION
    auto_populate_function = fields.Char(string='Original Values')
    #  # Define compute method to auto-populate employee_name based on employee_id
    @api.onchange('employee_number')

    def _compute_auto_populate(self):
        for record in self:
            if record.employee_number:
                auto_populate_record = self.env['hr.new.hire.trackers'].search([('employee_id', '=', record.employee_number)], limit=1)
                if auto_populate_record:
                    # Assigning values only if the fields are empty or haven't been modified
                    if not record.complete_name:
                        record.complete_name = auto_populate_record.complete_name
                    if not record.hire_date:
                        record.hire_date = auto_populate_record.hire_date
                    # if not record.c_employment_status:
                    #     record.c_employment_status = auto_populate_record.c_employment_status
                    if not record.c_entity:
                        record.c_entity = auto_populate_record.c_company
                    if not record.account:
                        record.account = auto_populate_record.account
                    if not record.position:
                        record.position = auto_populate_record.position
                    if not record.email_address:
                        record.email_address = auto_populate_record.work_email_address

                    # Store the initial values for future comparison
                    record.auto_populate_function = {
                        'complete_name': auto_populate_record.complete_name,
                        'hire_date': auto_populate_record.hire_date,
                        # 'c_employment_status': auto_populate_record.c_employment_status,
                        'c_entity': auto_populate_record.c_company,
                        'account': auto_populate_record.account,
                        'position': auto_populate_record.position,
                        'email_address': auto_populate_record.work_email_address,
                    }
                else:
                    pass
