import logging
import pytz
import threading
from collections import OrderedDict, defaultdict
from datetime import date, datetime, timedelta
# from psycopg2 import sql

from odoo import api, fields, models, tools, SUPERUSER_ID
from odoo.exceptions import UserError, AccessError
from odoo.osv import expression
from odoo.tools.translate import _
from odoo.tools import date_utils, email_re, email_split, is_html_empty, groupby
from odoo.tools.misc import get_lang
from random import randint
from odoo.exceptions import ValidationError

class NewHireTracker(models.Model):
    _name = 'hr.new.hire.trackers'
    _description = 'New Hire Trackers'
    _rec_name = 'employee_id'
    # _order = 'numeric_field DESC'
    
    active = fields.Boolean('Active', store=True, default=True, required=False)
    # numeric_field = fields.Integer(string="", compute="_compute_numeric_field", store=True, required=False)

    # HR Part
    employee_id = fields.Char('Employee ID', store=True, required=False)
    obt_number = fields.Char('OBT Number', store=True, required=False)
    tags = fields.Many2many('tags', string='Status', readonly=False, required=False, store=True)
    # qs_tags = fields.Char('QS Tags', store=True, required=False, compute='_compute_tag_names')

    # @api.depends('tags')
    # def _compute_tag_names(self):
    #     for record in self:
    #         record.qs_tags = ', '.join(record.tags.mapped('name'))

    # @api.constrains('employee_id', 'obt_number')
    # def _check_duplicate(self):
    #     for record in self:
    #         # Check if there are other records with the same employee_id
    #         if record.employee_id:
    #             duplicate_records = self.search([('employee_id', '=', record.employee_id), ('id', '!=', record.id)])
    #             if duplicate_records:
    #                 raise ValidationError('Employee Id already exists.')
    #         if record.obt_number:
    #             duplicate_records = self.search([('obt_number', '=', record.obt_number), ('id', '!=', record.id)])
    #             if duplicate_records:
    #                 raise ValidationError('OBT Number already exists.')
                
    recruiter = fields.Char('Recruiter', store=True, readonly=False, required=False)
    account = fields.Many2one('accounts', string='Account', store=True, readonly=False, required=False)
    hiring_manager = fields.Char('Hiring Manager', store=True, readonly=False, required=False)
    position = fields.Char('Position', store=True, readonly=False, required=False)
    c_classification_level = fields.Selection([('', ''), ('director', 'Director'), ('manager', 'Manager'), ('supervisor', 'Supervisor'), ('individual_contributor', 'Individual Contributor'), ('rank_file', 'Rank and File')],'Classification/Level', store=True,readonly=False, required=False)
    first_name = fields.Char('First Name', store=True, readonly=False, required=False)
    last_name = fields.Char('Last Name', store=True, readonly=False, required=False)
    c_employment_status = fields.Selection([('', ''),('probationary', 'Probationary'), ('regular', 'Regular'), ('project_based', 'Project-based'), ('currently_employed', 'Currently Employed')],'Employment Status', store=True, readonly=False, required=False)
    operation_start_date = fields.Date('Operation Start Date', store=True, readonly=False, required=False)
    neo_date = fields.Date('NEO Date', store=True)
    official_start_date = fields.Date('Official Start Date', store=True, readonly=False, required=False)
    default_shift = fields.Char('Default Shift', store=True, readonly=False, required=False)
    contact_details = fields.Char('Primary Mobile Number', store=True, readonly=False, required=False, compute='_compute_formatted_phone_number',)
    secondary_formatted_phone_number = fields.Char('Secondary Mobile Number', store=True, readonly=False, required=False)

    # LIMITED CHARACTERS IS ONLY ACCEPETED
    # @api.constrains('contact_details')
    # def _check_phone_number_length(self):
    #     for record in self:
    #         if record.contact_details and len(record.contact_details) != 13:
    #             raise ValidationError("Formatted phone number must be 11 characters.")

    @api.onchange('contact_details')
    def _compute_formatted_phone_number(self):
        for record in self:
            if record.contact_details and isinstance(record.contact_details, str) and record.contact_details.isdigit():
                formatted_number = f"{record.contact_details[:3]}-{record.contact_details[3:6]}-{record.contact_details[6:]}"
                
                # Check if the phone number starts with '0' before adding it
                if not formatted_number.startswith('0'):
                    formatted_number = '0' + formatted_number
                
                record.contact_details = formatted_number
            else:
                # Handle non-numeric phone numbers or empty values
                record.contact_details = record.contact_details

    @api.onchange('secondary_formatted_phone_number')
    def _compute_secondary_formatted_phone_number(self):
        for record in self:
            if record.secondary_formatted_phone_number == "N/A":
                # Handle "N/A" case
                pass
            else:
                if record.secondary_formatted_phone_number and isinstance(record.secondary_formatted_phone_number, str) and record.secondary_formatted_phone_number.isdigit():
                    formatted_number = f"{record.secondary_formatted_phone_number[:3]}-{record.secondary_formatted_phone_number[3:6]}-{record.secondary_formatted_phone_number[6:]}"
                    
                    # Check if the phone number starts with '0' before adding it
                    if not formatted_number.startswith('0'):
                        formatted_number = '0' + formatted_number
                    
                    record.secondary_formatted_phone_number = formatted_number
                else:
                    # Handle non-numeric phone numbers or empty values
                    record.secondary_formatted_phone_number = record.secondary_formatted_phone_number

    personal_email_address = fields.Char('Personal Email Address', store=True, readonly=False, required=False)
    work_email_address = fields.Char('Work Email Address', store=True, required=False)
    working_onsite = fields.Char('Working Onsite?', store=True, readonly=False, required=False)
    c_company = fields.Selection([('isupport_worldwide', 'iSupport Worldwide'), ('iswerk', 'ISWerk')], 'Company', store=True, readonly=False, required=False)
    job_offer = fields.Char('Job Offer', store=True, required=False)
    ok_to_start = fields.Char('OK to Start?', store=True, required=False)
    resgination_letter = fields.Char('Relieving Letter/Acceptance of Resignation Letter', store=True, required=False)


    completed_neo = fields.Char('Completed NEO', store=True, required=False)
    pc_laptop_details_sent = fields.Char('PC/Laptop Details Sent?', store=True, required=False)
    vaccination = fields.Char('Vaccination', store=True)
    neo_invite = fields.Char('NEO Invite', store=True, required=False)
    neo_acknowledgement_checklist = fields.Char('NEO Acknowledgement Checklist', store=True, required=False)
    handbook_acknowledgement = fields.Char('Handbook Acknowledgement', store=True, required=False)
    contract_type = fields.Char('Type of Contract', store=True, required=False)
    contract_status = fields.Char('Type of Contract Status', store=True, required=False)
    id_released = fields.Char('ID Released?', store=True, required=False)
    training_details = fields.Char('Training Details', store=True, required=False)
    date_enrolled = fields.Date('Date Enrolled', store=True, required=False)
    enrolled_by = fields.Char('Enrolled By', store=True, required=False)
    pay_type_remarks = fields.Text('Pay Type Remarks', store=True, required=False)
    government_remarks = fields.Text('Government Remarks', store=True, required=False)
    personal_info_remrks = fields.Text('Personal Info Remarks', store=True, required=False)
    esetting_remarks = fields.Text('Multiplier Remarks', store=True, required=False)
    validated_by = fields.Char('Validated By', store=True, required=False)
    validation_date = fields.Date('Validation Date', store=True, required=False)
    overall_remarks = fields.Text('Overall Remarks', store=True, required=False)

    # HR Part Extra
    middle_name = fields.Char('Middle Name', store=True, readonly=False, required=False)
    complete_name = fields.Char('Complete Name', store=True, compute='_compute_complete_name', readonly=False, required=False)

    @api.depends('first_name', 'last_name', 'middle_name')
    def _compute_complete_name(self): 
        for record in self:
            if record.first_name and record.last_name:
                record.complete_name = record.first_name + ' ' + record.last_name
            else:
                record.complete_name = False
                # record.middle_name + 

    # Requirements
    peme = fields.Char('PEME', store=True, required=False)
    peme_endorsement = fields.Char('PEME Endorsement', store=True, required=False)
    peme_clinic = fields.Char('PEME Clinic?', store=True, required=False)

    peme_date_of_examination = fields.Date('Date of Examination', store=True, required=False)
    peme_validity = fields.Date('Validity', store=True, required=False)
    peme_days_left = fields.Char('Days Left', store=True, required=False)

    nbi_clearance = fields.Char('NBI', store=True, required=False)
    government_documents = fields.Char('Government Documents', store=True, required=False)
    c_birth_certificate = fields.Selection([('done', 'Done'),('pending', 'Pending'), ('submitted', 'Submitted'), ('submitted(nso)', 'Submitted (NSO)')],'Birth Certificate', store=True, required=False)
    c_pic_2x2 = fields.Selection([('done', 'Done'),('pending', 'Pending'), ('submitted', 'Submitted')],'2x2', store=True, required=False)
    bir_2316 = fields.Char('BIR 2316', store=True, required=False)
    bir_2316_endorsement_date = fields.Date('BIR 2316 Endorsement Date', store=True, required=False)
    isp = fields.Char('ISP', store=True, required=False)
    coe = fields.Char('COE', store=True, required=False)
    onboarding_forms = fields.Char('Onboarding Forms', store=True, required=False)
    onboarding_requirement_email = fields.Char('Onboarding Requirement Email', store=True, required=False)
    deadline_of_primary_requirements = fields.Char('Deadline of Primary Requirements', store=True, required=False)
    deadline_of_secondary_requirements = fields.Char('Deadline of Secondary Requirements', store=True, required=False)
    letter_of_undertaking = fields.Char('Letter of Undertaking', store=True, required=False)
    remarks = fields.Char('Remarks', store=True, required=False)
    requirement_status = fields.Char('Requirement Status', store=True, required=False)

    # Additional Field
    hire_date = fields.Date('Hire Date', store=True, required=False)
    deadline = fields.Date('Deadline', store=True, required=False)

    # USED FOR THE AUTO-POPULATE FUNCTION
    auto_populate_function = fields.Char(string='Original Values')
    # Define compute method to auto-populate employee_name based on employee_id
    # INCLUDE THIS IN ANY FIELD FOR AUTO POPULATION
    # , compute = '_compute_auto_populate'

    # @api.onchange('obt_number')

    # def _compute_auto_populate(self):
    #     for record in self:
    #         if record.obt_number:
    #             auto_populate_record = self.env['hr.employee.onboarding.tracker'].search([('employee_id', '=', record.obt_number)], limit=1)
    #             if auto_populate_record:
    #                 # Assigning values only if the fields are empty or haven't been modified
    #                 if not record.recruiter:
    #                     record.recruiter = auto_populate_record.recruiter
    #                 if not record.account:
    #                     record.account = auto_populate_record.account
    #                 if not record.hiring_manager:
    #                     record.hiring_manager = auto_populate_record.hiring_manager
    #                 if not record.position:
    #                     record.position = auto_populate_record.position
    #                 if not record.c_classification_level:
    #                     record.c_classification_level = auto_populate_record.c_classification_level
    #                 if not record.first_name:
    #                     record.first_name = auto_populate_record.first_name
    #                 if not record.last_name:
    #                     record.last_name = auto_populate_record.last_name
    #                 if not record.c_employment_status:
    #                     record.c_employment_status = auto_populate_record.c_employment_status
    #                 if not record.operation_start_date:
    #                     record.operation_start_date = auto_populate_record.date_of_first_day_of_operations
    #                 if not record.neo_date:
    #                     record.neo_date = auto_populate_record.orientation_date
    #                 if not record.official_start_date:
    #                     record.official_start_date = auto_populate_record.actual_start_date
    #                 if not record.default_shift:
    #                     record.default_shift = auto_populate_record.training_schedule_default_shift
    #                 if not record.contact_details:
    #                     record.contact_details = auto_populate_record.mobile_number
    #                 if not record.secondary_formatted_phone_number:
    #                     record.secondary_formatted_phone_number = auto_populate_record.secondary_formatted_phone_number
    #                 if not record.personal_email_address:
    #                     record.personal_email_address = auto_populate_record.email
    #                 if not record.working_onsite:
    #                     record.working_onsite = auto_populate_record.working_onsite
    #                 if not record.c_company:
    #                     record.c_company = auto_populate_record.c_company
    #                 if not record.middle_name:
    #                     record.middle_name = auto_populate_record.middle_name
    #                 if not record.complete_name:
    #                     record.complete_name = auto_populate_record.complete_name
                    
    #                 # Handling Many2many field (tags)
    #                 # if not record.tags:
    #                 #     record.tags = [(6, 0, auto_populate_record.tags.ids)]  # Use a list of tuples (operation, values)
    

    #                 # Store the initial values for future comparison
    #                 record.auto_populate_function = {
    #                     'recruiter': auto_populate_record.recruiter,
    #                     'account': auto_populate_record.account,
    #                     'hiring_manager': auto_populate_record.hiring_manager,
    #                     'position': auto_populate_record.position,
    #                     'c_classification_level': auto_populate_record.c_classification_level,
    #                     'first_name': auto_populate_record.first_name,
    #                     'last_name': auto_populate_record.last_name,
    #                     'c_employment_status': auto_populate_record.c_employment_status,
    #                     'operation_start_date': auto_populate_record.date_of_first_day_of_operations,
    #                     'neo_date': auto_populate_record.orientation_date,
    #                     'official_start_date': auto_populate_record.actual_start_date,
    #                     'default_shift': auto_populate_record.training_schedule_default_shift,
    #                     'contact_details': auto_populate_record.mobile_number,
    #                     'secondary_formatted_phone_number': auto_populate_record.secondary_formatted_phone_number,
    #                     'personal_email_address': auto_populate_record.email,
    #                     'working_onsite': auto_populate_record.working_onsite,
    #                     'c_company': auto_populate_record.c_company,
    #                     'middle_name': auto_populate_record.middle_name,
    #                     'complete_name': auto_populate_record.complete_name,
    #                     # 'tags' : [(6, 0, auto_populate_record.tags.ids)], # Use a list of tuples (operation, values)
    #                 }
    #             else:
    #                 # Clear the fields if no matching record is found
    #                 # record.original_values = {}
    #                 # record.recruiter = ''
    #                 # record.tags = [(5, 0, 0)]  # Clearing Many2many field
    #                 pass
