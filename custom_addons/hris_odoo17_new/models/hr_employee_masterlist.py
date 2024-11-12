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

# class HR_Employee_Masterlist_Active(models.Model):
#     _name = 'hr.employee.masterlist.active'
#     _description = 'HR Employee Masterlist Active'
    # _rec_name = 'employee_id'

    # active = fields.Boolean('Active', store=True, default=True)
    # employee_id = fields.Char('Employee ID', store=True)
    #  # Employee ID VALIDATION ERROR
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
    # middle_name = fields.Char('Middle Name', store=True, readonly=False)
    # complete_name = fields.Char(string='Complete Name', compute='_compute_complete_name', store=True)
    # start_date = fields.Date('Start Date', store=True, readonly=False)
    # date_of_birth = fields.Date('Date of Birth', store=True)
    # department = fields.Selection([('', ''),('operations', 'OPERATIONS'),('support', 'SUPPORT')],'Department', store=True, index=True)
    # account = fields.Many2one('accounts', string='Account', store=True, readonly=False)
    # position = fields.Char('Position', store=True, readonly=False)
    # lob = fields.Char('LOB', store=True)
    # employee_address = fields.Text('Employee Address', store=True)
    # city = fields.Char('City', store=True)
    # region = fields.Char('Region', store=True)
    # employee_email_address = fields.Char('Employee Email Address', store=True, readonly=False)
    # mobile_number = fields.Char('Primary Mobile Number', store=True, readonly=False, compute='_compute_formatted_phone_number',)
    # secondary_formatted_phone_number = fields.Char('Secondary Phone Number', store=True, readonly=False)
    # landline_number = fields.Char('Landline Number', store=True, readonly=False)

    # # @api.constrains('mobile_number')
    # # def _check_phone_number_length(self):
    # #     for record in self:
    # #         if record.mobile_number and len(record.mobile_number) != 13:
    # #             raise ValidationError("Formatted phone number must be 11 characters.")

    # @api.onchange('mobile_number')
    # def _compute_formatted_phone_number(self):
    #     for record in self:
    #         if record.mobile_number and isinstance(record.mobile_number, str) and record.mobile_number.isdigit():
    #             formatted_number = f"{record.mobile_number[:3]}-{record.mobile_number[3:6]}-{record.mobile_number[6:]}"
                
    #             # Check if the phone number starts with '0' before adding it
    #             if not formatted_number.startswith('0'):
    #                 formatted_number = '0' + formatted_number
                
    #             record.mobile_number = formatted_number
    #         else:
    #             # Handle non-numeric phone numbers or empty values
    #             record.mobile_number = record.mobile_number

    # @api.onchange('secondary_formatted_phone_number')
    # def _compute_secondary_formatted_phone_number(self):
    #     for record in self:
    #         if record.secondary_formatted_phone_number == "N/A":
    #             # Handle "N/A" case
    #             pass
    #         else:
    #             if record.secondary_formatted_phone_number and isinstance(record.secondary_formatted_phone_number, str) and record.secondary_formatted_phone_number.isdigit():
    #                 formatted_number = f"{record.secondary_formatted_phone_number[:3]}-{record.secondary_formatted_phone_number[3:6]}-{record.secondary_formatted_phone_number[6:]}"
                    
    #                 # Check if the phone number starts with '0' before adding it
    #                 if not formatted_number.startswith('0'):
    #                     formatted_number = '0' + formatted_number
                    
    #                 record.secondary_formatted_phone_number = formatted_number
    #             else:
    #                 # Handle non-numeric phone numbers or empty values
    #                 record.secondary_formatted_phone_number = record.secondary_formatted_phone_number
    
    # # 2nd lob optional
    # second_lob = fields.Char('LOB', store=True)

    # payroll_approver = fields.Char('Payroll Approver', store=True)
    # payroll_approvers_email_address = fields.Char('Payroll Approvers Email Address', store=True)
    # managers_name = fields.Char('Managers Name', store=True)
    # managers_email_address = fields.Char('Managers Email Address', store=True)
    # performance_review_poc = fields.Char('Performance Review POC', store=True)
    # internet_provider = fields.Char('Internet Provider', store=True)
    # company = fields.Selection([('isupport_worldwide', 'iSupport Worldwide'), ('iswerk','ISWerk')], 'Company', store=True, readonly=False)
    # entity_updated = fields.Date('Entity Updated', store=True)
    # all_employees_except_pmi = fields.Char('All Employees except PMI', store=True)
    # isupport_employees_distro = fields.Char('iSupport Employees Distro', store=True)
    # iswerk_employees_distro = fields.Char('iSWerk Employees Distro', store=True)
    # all_sanmar = fields.Char('All Sanmar', store=True)
    # all_ammex = fields.Char('All Ammex', store=True)
    # lighthouse = fields.Char('LightHouse', store=True)
    # isupporthub = fields.Char('iSupportHub', store=True)

    # @api.depends('last_name', 'first_name', 'middle_name')
    # def _compute_complete_name(self):
    #     for record in self:
    #         name_parts = [part for part in [record.first_name, record.middle_name, record.last_name] if part]
    #         record.complete_name = ' '.join(name_parts)
    
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
    #                 if not record.middle_name:
    #                     record.middle_name = auto_populate_record.middle_name
    #                 if not record.start_date:
    #                     record.start_date = auto_populate_record.official_start_date
    #                 if not record.account:
    #                     record.account = auto_populate_record.account
    #                 if not record.position:
    #                     record.position = auto_populate_record.position
    #                 if not record.employee_email_address:
    #                     record.employee_email_address = auto_populate_record.work_email_address
    #                 if not record.mobile_number:
    #                     record.mobile_number = auto_populate_record.contact_details
    #                 if not record.secondary_formatted_phone_number:
    #                     record.secondary_formatted_phone_number = auto_populate_record.secondary_formatted_phone_number
    #                 if not record.company:
    #                     record.company = auto_populate_record.c_company

    #                 # Store the initial values for future comparison
    #                 record.auto_populate_function = {
    #                     'first_name': auto_populate_record.first_name,
    #                     'last_name': auto_populate_record.last_name,
    #                     'middle_name': auto_populate_record.middle_name,
    #                     'start_date': auto_populate_record.official_start_date,
    #                     'account': auto_populate_record.account,
    #                     'position': auto_populate_record.position,
    #                     'employee_email_address': auto_populate_record.work_email_address,
    #                     'mobile_number': auto_populate_record.contact_details,
    #                     'secondary_formatted_phone_number': auto_populate_record.secondary_formatted_phone_number,
    #                     'company': auto_populate_record.c_company,
    #                 }
    #             else:
    #                 pass


# class HR_Employee_Masterlist_Inactive(models.Model):
#     _name = 'hr.employee.masterlist.inactive'
#     _description = 'HR Employee Masterlist Inactive'
    # _rec_name = 'eid'

    # active = fields.Boolean('Active', store=True, default=True)
    # eid = fields.Char('EID', store=True)
    #  # Employee ID VALIDATION ERROR
    # @api.constrains('eid')
    # def _check_duplicate(self):
    #     for record in self:
    #         # Check if there are other records with the same employee_id
    #         if record.eid:
    #             duplicate_records = self.search([('eid', '=', record.eid), ('id', '!=', record.id)])
    #             if duplicate_records:
    #                 raise ValidationError('Employee Id already exists.')    
                
    # department_account = fields.Many2one('accounts', string='Account', store=True, readonly=False)
    # first_name = fields.Char('First Name', store=True, readonly=False)
    # last_name = fields.Char('Last Name', store=True, readonly=False)
    # middle_name = fields.Char('Middle Name', store=True, readonly=False)
    # complete_name = fields.Char('Complete Name', store=True, compute='_compute_complete_name')
    # hire_date = fields.Date('Hire Date', store=True, index=True, readonly=False)
    # start_date = fields.Date('Start Date', store=True, readonly=False)
    # date_of_birth = fields.Date('Date of Birth', store=True)
    # department = fields.Selection([('', ''),('operations', 'OPERATIONS'),('support', 'SUPPORT')],'Department', store=True, index=True) 
    # position = fields.Char('Position', store=True, readonly=False)
    # employee_address = fields.Text('Employee Address', store=True)
    # city = fields.Char('City', store=True)
    # region = fields.Char('Region', store=True)
    # employee_email_address = fields.Char('Employee Email Address', store=True, readonly=False)
    # mobile_number = fields.Char('Primary Mobile Number', store=True, readonly=False, compute='_compute_formatted_phone_number',)
    # secondary_formatted_phone_number = fields.Char('Secondary Phone Number', store=True, readonly=False)
    # landline_number = fields.Char('Landline Number', store=True, readonly=False)

    # # @api.constrains('mobile_number')
    # # def _check_phone_number_length(self):
    # #     for record in self:
    # #         if record.mobile_number and len(record.mobile_number) != 13:
    # #             raise ValidationError("Formatted phone number must be 11 characters.")

    # @api.onchange('mobile_number')
    # def _compute_formatted_phone_number(self):
    #     for record in self:
    #         if record.mobile_number and isinstance(record.mobile_number, str) and record.mobile_number.isdigit():
    #             formatted_number = f"{record.mobile_number[:3]}-{record.mobile_number[3:6]}-{record.mobile_number[6:]}"
                
    #             # Check if the phone number starts with '0' before adding it
    #             if not formatted_number.startswith('0'):
    #                 formatted_number = '0' + formatted_number
                
    #             record.mobile_number = formatted_number
    #         else:
    #             # Handle non-numeric phone numbers or empty values
    #             record.mobile_number = record.mobile_number

    # @api.onchange('secondary_formatted_phone_number')
    # def _compute_secondary_formatted_phone_number(self):
    #     for record in self:
    #         if record.secondary_formatted_phone_number == "N/A":
    #             # Handle "N/A" case
    #             pass
    #         else:
    #             if record.secondary_formatted_phone_number and isinstance(record.secondary_formatted_phone_number, str) and record.secondary_formatted_phone_number.isdigit():
    #                 formatted_number = f"{record.secondary_formatted_phone_number[:3]}-{record.secondary_formatted_phone_number[3:6]}-{record.secondary_formatted_phone_number[6:]}"
                    
    #                 # Check if the phone number starts with '0' before adding it
    #                 if not formatted_number.startswith('0'):
    #                     formatted_number = '0' + formatted_number
                    
    #                 record.secondary_formatted_phone_number = formatted_number
    #             else:
    #                 # Handle non-numeric phone numbers or empty values
    #                 record.secondary_formatted_phone_number = record.secondary_formatted_phone_number

    # payroll_approver = fields.Char('Payroll Approver', store=True)
    # payroll_approvers_email_address = fields.Char('Payroll Approver\'s Email Address', store=True)
    # managers_name = fields.Char('Manager\'s Name', store=True)
    # managers_email_address = fields.Char('Manager\'s Email Address', store=True)
    # performance_review_poc = fields.Char('Performance Review POC', store=True)
    # internet_provider = fields.Char('Internet Provider', store=True)
    # company = fields.Selection([('', ''), ('isupport_worldwide', 'Isupport Worldwide'), ('iswerk','ISWerk')], 'Company', store=True, readonly=False)
    # category = fields.Selection([('desired', 'Desired'), ('undesired','Undesired'), ('authorized','Authorized')],'Category Selection', store=True)
    # lob = fields.Char('LOB', store=True)
    # seperation_date = fields.Date('Seperation Date', store=True)
    # seperation_status = fields.Char('Seperation Status', store=True)
    # reason_for_seperation = fields.Text('Reason for Seperation(Resignation Letter)', store=True)
    # @api.depends('last_name', 'first_name', 'middle_name')
    # def _compute_complete_name(self):
    #     for record in self:
    #         name_parts = [part for part in [record.first_name, record.middle_name, record.last_name] if part]
    #         record.complete_name = ' '.join(name_parts)

    # # USED FOR THE AUTO-POPULATE FUNCTION
    # auto_populate_function = fields.Char(string='Original Values')
    # #  # Define compute method to auto-populate employee_name based on employee_id
    # @api.onchange('eid')

    # def _compute_auto_populate(self):
    #     for record in self:
    #         if record.eid:
    #             auto_populate_record = self.env['hr.new.hire.trackers'].search([('employee_id', '=', record.eid)], limit=1)
    #             if auto_populate_record:
    #                 # Assigning values only if the fields are empty or haven't been modified
    #                 if not record.department_account:
    #                     record.department_account = auto_populate_record.account
    #                 if not record.first_name:
    #                     record.first_name = auto_populate_record.first_name
    #                 if not record.last_name:
    #                     record.last_name = auto_populate_record.last_name
    #                 if not record.middle_name:
    #                     record.middle_name = auto_populate_record.middle_name
    #                 if not record.hire_date:
    #                     record.hire_date = auto_populate_record.hire_date
    #                 if not record.start_date:
    #                     record.start_date = auto_populate_record.official_start_date
    #                 if not record.position:
    #                     record.position = auto_populate_record.position
    #                 if not record.employee_email_address:
    #                     record.employee_email_address = auto_populate_record.work_email_address
    #                 if not record.mobile_number:
    #                     record.mobile_number = auto_populate_record.contact_details
    #                 if not record.secondary_formatted_phone_number:
    #                     record.secondary_formatted_phone_number = auto_populate_record.secondary_formatted_phone_number
    #                 if not record.company:
    #                     record.company = auto_populate_record.c_company

    #                 # Store the initial values for future comparison
    #                 record.auto_populate_function = {
    #                     'department_account': auto_populate_record.account,
    #                     'first_name': auto_populate_record.first_name,
    #                     'last_name': auto_populate_record.last_name,
    #                     'middle_name': auto_populate_record.middle_name,
    #                     'hire_date': auto_populate_record.hire_date,
    #                     'start_date': auto_populate_record.official_start_date,
    #                     'position': auto_populate_record.position,
    #                     'employee_email_address': auto_populate_record.work_email_address,
    #                     'mobile_number': auto_populate_record.contact_details,
    #                     'secondary_formatted_phone_number': auto_populate_record.secondary_formatted_phone_number,
    #                     'company': auto_populate_record.c_company,
    #                 }
    #             else:
    #                 pass

# class HR_Employee_Masterlist_ResignationTracker(models.Model):
#     _name = 'hr.employee.masterlist.resignation.tracker'
#     _description = 'HR Employee Masterlist Resignation Tracker'
    # _rec_name = 'id_no'    

    # active = fields.Boolean('Active', store=True, default=True)
    # id_no = fields.Char('ID Number', store=True)
    # # Employee ID VALIDATION ERROR
    # @api.constrains('id_no')
    # def _check_duplicate(self):
    #     for record in self:
    #         # Check if there are other records with the same employee_id
    #         if record.id_no:
    #             duplicate_records = self.search([('id_no', '=', record.id_no), ('id', '!=', record.id)])
    #             if duplicate_records:
    #                 raise ValidationError('Employee Id already exists.')      
                
    # fullname = fields.Char('Full Name', store=True, readonly=False)
    # department = fields.Many2one('accounts', string='Department', store=True, readonly=False)
    # position = fields.Char('Position', store=True, readonly=False)
    # c_employment_status = fields.Selection([('', ''),('probationary', 'PROBATIONARY'), ('regular', 'REGULAR'), ('project_based', 'PROJECT-BASED')],'Employment Status', store=True)
    # date_hired = fields.Date('Date Hired', store=True, readonly=False)
    # seperation_date = fields.Date('Seperation Date', store=True)
    # seperation_status = fields.Selection([('deceased', 'Deceased'), ('end_of_project', 'END OF PROJECT'), ('non_regularization', 'NON-REGULARIZATION'), 
    #                                       ('redundate','REDUNDATE'), ('resigned', 'RESIGNED'), ('retrenched', 'RETRENCHED'), ('terminated', 'TERMINATED')],'Seperation Status', store=True)
    # category = fields.Selection([('desired', 'Desired'), ('undesired','Undesired'), ('authorized','Authorized')],'Category', store=True)
    # c_reason_for_seperation = fields.Selection([('personal_reason_undefined', 'Personal Reason/ Undefined'), ('career_growth_role_expansion', 'Career Growth/Role Expansion'), 
    #                                             ('redundancy', 'Redundancy'), ('performance','Performance'), ('better_compensation_package', 'Better Compensation Package'), 
    #                                             ('health_reason', 'Health Reason'), ('resigned_in_liue_of_termination_violation', 'RESIGNED in liue of termination (violation)'), 
    #                                             ('resigned_in_liue_of_possible_termination_awol', 'RESIGNED in liue of possible termination (AWOL)'), ('resigned_in_liue_of_termination_non_regularization', 'RESIGNED in liue of termination (non-regularization)'),
    #                                             ('end_of_project', 'End Of Project') , ('family_matters', 'Family Matters'), ('not_satisfied-with_type_of_work_account_processes', 'Not Satisfied with type of work/ account/process'), 
    #                                             ('change_of_career', 'Change Of Career') , ('termination_violation', 'Termination-Violation') , ('permanent_wfh_set_up', 'Permanent WFH set up') , ('relocation', 'Relocation'), 
    #                                             ('permanent_day_shift_schedule', 'Permanent Day Shift Schedule') , ('deceased', 'Deceased') , ('job_abandonment', 'Job Abandonment') , ('rto_concerns', 'RTO Concerns'), 
    #                                             ('career_growth', 'Career Growth'), ('termination_due_to_ncns', 'Termination Due to NCNS'), ('transfer_to_satellite_office', 'Transfer to Satellite Office'), 
    #                                             ('bda_redundancy', 'BDA Redundancy') , ('pursue_further_studies', 'Pursue further Studies')], 'Reason For Separation (Resignation Letter/ Termination Notice)', store=True)
    # voluntary_involuntary = fields.Selection([('voluntary', 'VOLUNTARY'), ('involuntary','INVOLUNTARY')], 'Voluntary/Involuntary', store=True)
    # retention_call = fields.Char('Retention Call', store=True)
    # exit_report = fields.Text('Exit Report', store=True)

    # # USED FOR THE AUTO-POPULATE FUNCTION
    # auto_populate_function = fields.Char(string='Original Values')
    # #  # Define compute method to auto-populate employee_name based on employee_id
    # @api.onchange('id_no')

    # def _compute_auto_populate(self):
    #     for record in self:
    #         if record.id_no:
    #             auto_populate_record = self.env['hr.new.hire.trackers'].search([('employee_id', '=', record.id_no)], limit=1)
    #             if auto_populate_record:
    #                 # Assigning values only if the fields are empty or haven't been modified
    #                 if not record.fullname:
    #                     record.fullname = auto_populate_record.complete_name
    #                 if not record.department:
    #                     record.department = auto_populate_record.account
    #                 if not record.position:
    #                     record.position = auto_populate_record.position
    #                 if not record.c_employment_status:
    #                     record.c_employment_status = auto_populate_record.c_employment_status
    #                 if not record.date_hired:
    #                     record.date_hired = auto_populate_record.hire_date

    #                 # Store the initial values for future comparison
    #                 record.auto_populate_function = {
    #                     'fullname': auto_populate_record.complete_name,
    #                     'department': auto_populate_record.account,
    #                     'position': auto_populate_record.position,
    #                     'c_employment_status': auto_populate_record.c_employment_status,
    #                     'date_hired': auto_populate_record.hire_date,
    #                 }
    #             else:
    #                 pass



