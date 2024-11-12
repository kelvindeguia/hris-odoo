# import logging
# import pytz
# import threading
# from collections import OrderedDict, defaultdict
# from datetime import date, datetime, timedelta
# # from psycopg2 import sql

# from odoo import api, fields, models, tools, SUPERUSER_ID
# from odoo.exceptions import UserError, AccessError
# from odoo.osv import expression
# from odoo.tools.translate import _
# from odoo.tools import date_utils, email_re, email_split, is_html_empty, groupby
# from odoo.tools.misc import get_lang
# from random import randint
# from odoo.exceptions import ValidationError

# # _logger = logging.getLogger(__name__)

# class HREmployeeCredentialsValidation_newhires(models.Model):
#     _name = 'hr.employee.credentials.validation.newhires'
#     _description = 'New Hires worksheet on Employee Credentials Validation'
#     _rec_name = 'employee_id'

#     active = fields.Boolean('Active', store=True, default=True)
#     date_enrolled = fields.Date('Date Enrolled', store=True)
#     c_entity = fields.Selection([('isupport_worldwide', 'iSupport Worldwide'), ('iswerk', 'ISWerk')],'Entity', store=True, readonly=False)
#     employee_id = fields.Char('Employee ID', store=True)

#     @api.constrains('employee_id')
#     def _check_duplicate(self):
#         for record in self:
#             # Check if there are other records with the same employee_id
#             if record.employee_id:
#                 duplicate_records = self.search([('employee_id', '=', record.employee_id), ('id', '!=', record.id)])
#                 if duplicate_records:
#                     raise ValidationError('Employee Id already exists.')

#     first_name = fields.Char('First Name', store=True, readonly=False, compute = '_compute_auto_populate')
#     last_name = fields.Char('Last Name', store=True, readonly=False)

#     account_department = fields.Many2one('accounts', string='Account/Department', store=True, readonly=False)
#     position = fields.Char('Position', store=True, readonly=False)
#     c_classification = fields.Selection([('', ''), ('director', 'Director'), ('manager', 'Manager'), ('supervisor', 'Supervisor'), ('individual_contributor', 'Individual Contributor'), ('rank_file', 'Rank and File')],'Classification', store=True, readonly=False)
#     c_employment_status = fields.Selection([('', ''),('probationary', 'Probationary'), ('regular', 'Regular'), ('project_based', 'Project-based'), ('currently_employed', 'Currently Employed')],'Employment Status', store=True, readonly=False)
#     operation_start_date = fields.Date('Operation Start Date', store=True, readonly=False)
#     orientation_date = fields.Date('Orientation Date', store=True, readonly=False)
#     default_shift = fields.Char('Default Shift', store=True, readonly=False)

#     contact_details = fields.Char('Contact Details', store=True, readonly=False, compute='_compute_formatted_phone_number')
#     secondary_formatted_phone_number = fields.Char('Secondary Phone Number', store=True, readonly=False)

#     # @api.constrains('contact_details')
#     # def _check_phone_number_length(self):
#     #     for record in self:
#     #         if record.contact_details and len(record.contact_details) != 13:
#     #             raise ValidationError("Formatted phone number must be 13 characters.")

#     @api.onchange('contact_details')
#     def _compute_formatted_phone_number(self):
#         for record in self:
#             if record.contact_details and isinstance(record.contact_details, str) and record.contact_details.isdigit():
#                 formatted_number = f"{record.contact_details[:3]}-{record.contact_details[3:6]}-{record.contact_details[6:]}"
                
#                 # Check if the phone number starts with '0' before adding it
#                 if not formatted_number.startswith('0'):
#                     formatted_number = '0' + formatted_number
                
#                 record.contact_details = formatted_number
#             else:
#                 # Handle non-numeric phone numbers or empty values
#                 record.contact_details = record.contact_details

#     @api.onchange('secondary_formatted_phone_number')
#     def _compute_secondary_formatted_phone_number(self):
#         for record in self:
#             if record.secondary_formatted_phone_number == "N/A":
#                 # Handle "N/A" case
#                 pass
#             else:
#                 if record.secondary_formatted_phone_number and isinstance(record.secondary_formatted_phone_number, str) and record.secondary_formatted_phone_number.isdigit():
#                     formatted_number = f"{record.secondary_formatted_phone_number[:3]}-{record.secondary_formatted_phone_number[3:6]}-{record.secondary_formatted_phone_number[6:]}"
                    
#                     # Check if the phone number starts with '0' before adding it
#                     if not formatted_number.startswith('0'):
#                         formatted_number = '0' + formatted_number
                    
#                     record.secondary_formatted_phone_number = formatted_number
#                 else:
#                     # Handle non-numeric phone numbers or empty values
#                     record.secondary_formatted_phone_number = record.secondary_formatted_phone_number
                    
#     email = fields.Char('Email', store=True, readonly=False)
#     enrolled_by = fields.Char('Enrolled By', store=True)
#     pay_type_remarks = fields.Text('Pay Type Remarks', store=True)
#     government_remarks = fields.Text('Government Remarks', store=True)
#     personal_info_remrks = fields.Text('Personal Info Remarks', store=True)
#     esetting_remarks = fields.Text('Multiplier Remarks', store=True)
#     validated_by = fields.Char('Validated By', store=True)
#     validation_date = fields.Date('Validation Date', store=True)
#     overall_remarks = fields.Text('Overall Remarks', store=True)
#     complete_name = fields.Char('Complete Name', store=True, compute='_compute_complete_name')
   
   
#     @api.depends('first_name', 'last_name')
#     def _compute_complete_name(self):
#         for record in self:
#             if record.first_name and record.last_name:
#                 record.complete_name = record.first_name + ' ' + record.last_name
#             else:
#                 record.complete_name = False

#     # USED FOR THE AUTO-POPULATE FUNCTION
#     auto_populate_function = fields.Char(string='Original Values')
#     #  # Define compute method to auto-populate employee_name based on employee_id
#     @api.onchange('employee_id')

#     def _compute_auto_populate(self):
#         for record in self:
#             if record.employee_id:
#                 auto_populate_record = self.env['hr.new.hire.trackers'].search([('employee_id', '=', record.employee_id)], limit=1)
#                 if auto_populate_record:
#                     # Assigning values only if the fields are empty or haven't been modified
#                     if not record.c_entity:
#                         record.c_entity = auto_populate_record.c_company
#                     if not record.first_name:
#                         record.first_name = auto_populate_record.first_name
#                     if not record.last_name:
#                         record.last_name = auto_populate_record.last_name
#                     if not record.account_department:
#                         record.account_department = auto_populate_record.account
#                     if not record.position:
#                         record.position = auto_populate_record.position
#                     if not record.c_classification:
#                         record.c_classification = auto_populate_record.c_classification_level
#                     if not record.c_employment_status:
#                         record.c_employment_status = auto_populate_record.c_employment_status
#                     if not record.operation_start_date:
#                         record.operation_start_date = auto_populate_record.operation_start_date
#                     if not record.orientation_date:
#                         record.orientation_date = auto_populate_record.neo_date
#                     if not record.default_shift:
#                         record.default_shift = auto_populate_record.default_shift
#                     if not record.contact_details:
#                         record.contact_details = auto_populate_record.contact_details
#                     if not record.secondary_formatted_phone_number:
#                         record.secondary_formatted_phone_number = auto_populate_record.secondary_formatted_phone_number
#                     if not record.email:
#                         record.email = auto_populate_record.work_email_address

#                     # Store the initial values for future comparison
#                     record.auto_populate_function = {
#                         'c_entity': auto_populate_record.c_company,
#                         'first_name': auto_populate_record.first_name,
#                         'last_name': auto_populate_record.last_name,
#                         'account_department': auto_populate_record.account,
#                         'position': auto_populate_record.position,
#                         'c_classification': auto_populate_record.c_classification_level,
#                         'c_employment_status': auto_populate_record.c_employment_status,
#                         'operation_start_date': auto_populate_record.operation_start_date,
#                         'orientation_date': auto_populate_record.neo_date,
#                         'default_shift': auto_populate_record.default_shift,
#                         'contact_details': auto_populate_record.contact_details,
#                         'secondary_formatted_phone_number': auto_populate_record.secondary_formatted_phone_number,
#                         'email': auto_populate_record.work_email_address,
#                     }
#                 else:
#                     pass

# class HREmployeeCredentialsValidation_govnumbers(models.Model):
#     _inherit = ['mail.thread', 'mail.activity.mixin', 'utm.mixin']
#     _name = 'hr.employee.credentials.validation.govnumbers'
#     _description = 'Pending Gov Numbers worksheet in Employee Credentials Validation'
#     _rec_name = 'employee_id'
    
#     active = fields.Boolean('Active', store=True, default=True)

#     employee_id = fields.Char('Employee ID',store=True)
#    # Employee ID VALIDATION ERROR
#     @api.constrains('employee_id')
#     def _check_duplicate(self):
#         for record in self:
#             # Check if there are other records with the same employee_id
#             if record.employee_id:
#                 duplicate_records = self.search([('employee_id', '=', record.employee_id), ('id', '!=', record.id)])
#                 if duplicate_records:
#                     raise ValidationError('Employee Id already exists.')        

#     first_name = fields.Char('First Name', store=True, readonly=False)
#     last_name = fields.Char('Last Name', store=True, readonly=False)
#     c_entity = fields.Selection([('isupport_worldwide', 'iSupport Worldwide'), ('iswerk', 'ISWerk')],'Entity', store=True, readonly=False)
#     sss = fields.Char('SSS', store=True)
#     phic = fields.Char('PHIC', store=True)
#     hdmf = fields.Char('HDMF', store=True)
#     tin = fields.Char('TIN', store=True)
#     remarks = fields.Text('Remarks', store=True)
#     complete_name = fields.Char('Complete Name', store=True, compute='_compute_complete_name')

#     # Field to indentify the email sending
#     send_email = fields.Boolean('Email Sent', store=True)

#     # Send Email Function
#     def send_email_function(self):
#         for record in self:
#             if record.send_email == False:
#                 record.sudo().write({'send_email': True})
#             if record.send_email == True:
#                 record.sudo().write({'send_email': False})    
            
   
#     @api.depends('first_name', 'last_name')
#     def _compute_complete_name(self):
#         for record in self:
#             if record.first_name and record.last_name:
#                 record.complete_name = record.first_name + ' ' + record.last_name
#             else:
#                 record.complete_name = False

    
#     # USED FOR THE AUTO-POPULATE FUNCTION
#     auto_populate_function = fields.Char(string='Original Values')

#      # Define compute method to auto-populate employee_name based on employee_id
#     @api.onchange('employee_id')

#     def _compute_auto_populate(self):
#         for record in self:
#             if record.employee_id:
#                 auto_populate_record = self.env['hr.new.hire.trackers'].search([('employee_id', '=', record.employee_id)], limit=1)
#                 if auto_populate_record:
#                     # Assigning values only if the fields are empty or haven't been modified
#                     if not record.first_name:
#                         record.first_name = auto_populate_record.first_name
#                     if not record.last_name:
#                         record.last_name = auto_populate_record.last_name
#                     if not record.c_entity:
#                         record.c_entity = auto_populate_record.c_company
#                     if not record.email:
#                         record.email = auto_populate_record.work_email_address

#                     # Store the initial values for future comparison
#                     record.auto_populate_function = {
#                         'first_name': auto_populate_record.first_name,
#                         'last_name': auto_populate_record.last_name,
#                         'c_entity': auto_populate_record.c_company,
#                         'email': auto_populate_record.work_email_address,
#                     }
#                 else:
#                     pass

#     email = fields.Char('Email', store=True, readonly=False)
  

# class HREmployeeCredentialsValidation_toiswerk(models.Model):
#     _name = 'hr.employee.credentials.validation.toiswerk'
#     _description = 'Transition to iSWerk worksheet in Employee Credentials Validation'
#     _rec_name = 'employee_id'
#     # _inherit = ['mail.thread']
    
#     active = fields.Boolean('Active', store=True, default=True)
#     date_enrolled = fields.Date('Date Enrolled', store=True)
#     enrolled_by = fields.Char('Enrolled By', store=True)
#     employee_id = fields.Char('Employee ID', store=True)
#     # Employee ID VALIDATION ERROR
#     @api.constrains('employee_id')
#     def _check_duplicate(self):
#         for record in self:
#             # Check if there are other records with the same employee_id
#             if record.employee_id:
#                 duplicate_records = self.search([('employee_id', '=', record.employee_id), ('id', '!=', record.id)])
#                 if duplicate_records:
#                     raise ValidationError('Employee Id already exists.')       

#     first_name = fields.Char('First Name', store=True, readonly=False)
#     last_name = fields.Char('Last Name', store=True, readonly=False)
#     # account_department = fields.Char('Account/Department', store=True, readonly=False)
#     account_department = fields.Selection([('',''),('operations','OPERATIONS'),('support','SUPPORT')], 'Account/Department', store=True, readonly=False)
#     position = fields.Char('Position', store=True, readonly=False)
#     complete_name = fields.Char('Complete Name', store=True, compute='_compute_complete_name')
   
#     @api.depends('first_name', 'last_name')
#     def _compute_complete_name(self):
#         for record in self:
#             if record.first_name and record.last_name:
#                 record.complete_name = record.first_name + ' ' + record.last_name
#             else:
#                 record.complete_name = False

#     # USED FOR THE AUTO-POPULATE FUNCTION
#     auto_populate_function = fields.Char(string='Original Values')

#      # Define compute method to auto-populate employee_name based on employee_id
#     @api.onchange('employee_id')

#     def _compute_auto_populate(self):
#         for record in self:
#             if record.employee_id:
#                 auto_populate_record = self.env['hr.new.hire.trackers'].search([('employee_id', '=', record.employee_id)], limit=1)
#                 if auto_populate_record:
#                     # Assigning values only if the fields are empty or haven't been modified
#                     if not record.first_name:
#                         record.first_name = auto_populate_record.first_name
#                     if not record.last_name:
#                         record.last_name = auto_populate_record.last_name
#                     if not record.position:
#                         record.position = auto_populate_record.position

#                     # Store the initial values for future comparison
#                     record.auto_populate_function = {
#                         'first_name': auto_populate_record.first_name,
#                         'last_name': auto_populate_record.last_name,
#                         'position': auto_populate_record.position,
#                     }
#                 else:
#                     pass