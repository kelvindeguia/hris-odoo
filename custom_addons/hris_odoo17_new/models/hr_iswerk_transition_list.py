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


class HR_Iswerk_Transition_list(models.Model):
    _name = 'hr.iswerk.transition.list'
    _description = 'Iswerk Transition List'
    _rec_name = 'employee_id'

    active = fields.Boolean('Active', store=True, default=True)

    employee_id = fields.Char('Employee ID', store=True, index=True)
    # Employee ID VALIDATION ERROR
    @api.constrains('employee_id')
    def _check_duplicate(self):
        for record in self:
            # Check if there are other records with the same employee_id
            if record.employee_id:
                duplicate_records = self.search([('employee_id', '=', record.employee_id), ('id', '!=', record.id)])
                if duplicate_records:
                    raise ValidationError('Employee Id already exists.')    
                  
    complete_name = fields.Char('Complete Name', store=True, index=True, readonly=False)
    position = fields.Char('Position', store=True, index=True, readonly=False)
    start_date = fields.Date('Start Date', store=True, index=True, readonly=False)
    department_account = fields.Many2one('accounts', string='Department/Account', store=True, index=True, readonly=False)
    work_email = fields.Char('Work Email', store=True, index=True, readonly=False)
    effective_date_transfer = fields.Date('Effective Date Transfer')
    payroll_credential_status = fields.Selection([('done', 'Done'), ('pending', 'Pending'), ('','')], store=True)
    payroll_enrolled_date = fields.Date('Payroll Enrolled Date')
    payroll_credential_generated_by = fields.Char('Payroll Credential Generated By')
    validated_by = fields.Char('Validated By')

    # USED FOR THE AUTO-POPULATE FUNCTION
    auto_populate_function = fields.Char(string='Original Values')
    #  # Define compute method to auto-populate employee_name based on employee_id
    @api.onchange('employee_id')

    def _compute_auto_populate(self):
        for record in self:
            if record.employee_id:
                auto_populate_record = self.env['hr.new.hire.trackers'].search([('employee_id', '=', record.employee_id)], limit=1)
                if auto_populate_record:
                    # Assigning values only if the fields are empty or haven't been modified
                    if not record.complete_name:
                        record.complete_name = auto_populate_record.complete_name
                    if not record.position:
                        record.position = auto_populate_record.position
                    if not record.start_date:
                        record.start_date = auto_populate_record.official_start_date
                    if not record.department_account:
                        record.department_account = auto_populate_record.account
                    if not record.work_email:
                        record.work_email = auto_populate_record.work_email_address

                    # Store the initial values for future comparison
                    record.auto_populate_function = {
                        'complete_name': auto_populate_record.complete_name,
                        'position': auto_populate_record.position,
                        'start_date': auto_populate_record.official_start_date,
                        'department_account': auto_populate_record.account,
                        'work_email': auto_populate_record.work_email_address,
                    }
                else:
                    pass

