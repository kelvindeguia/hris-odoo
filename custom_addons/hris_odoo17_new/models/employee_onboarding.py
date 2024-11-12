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

# class HREmployeeOnboardingTrackersss(models.Model):
#     _name = 'hr.employee.onboarding.trackersss'
#     _description = 'Employee Onboarding Trackersss'
    # _rec_name = 'employee_id'

    # # Green Part
    # active = fields.Boolean('Active', store=True, default=True, required=False)
    # sequence = fields.Integer('Sequence', store = True)

    # # Employee No./ID = OBT Num
    # employee_id = fields.Char('Employee Number', store=True, required=False)
    # @api.constrains('employee_id')
    # def _check_duplicate_employee_id(self):
    #     for record in self:
    #         # Check if there are other records with the same employee_id
    #         if record.employee_id:
    #             duplicate_records = self.search([('employee_id', '=', record.employee_id), ('id', '!=', record.id)])
    #             if duplicate_records:
    #                 raise ValidationError('Employee Number already exists.')
                
    # # Fallout Tag / Status
    # tags = fields.Many2many('tags', string='Status', required=False)
    # @api.constrains('tags')
    # def _check_tags_limit(self):
    #     for record in self:
    #         if len(record.tags) > 1:
    #             raise ValidationError("Only one status can be selected.")

    # request_id = fields.Char('Req ID', store=True, required=False)
    # account = fields.Many2one('accounts', string='Account', store=True, required=False)
    # first_name = fields.Char('First Name', store=True, required=False)
    # middle_name = fields.Char('Middle Name', store=True, required=False)
    # last_name = fields.Char('Last Name', store=True, required=False)
    # nickname = fields.Char('Nickname', store=True, required=False)
    # job_offer_date = fields.Date('Job Offer Date', store=True, required=False)
    # recruiter = fields.Char('Recruiter', store=True, required=False)
    # hiring_manager = fields.Char('Hiring Manager', store=True, required=False)
    # position = fields.Char('Position', store=True, required=False)
    # hiring_type = fields.Char('Hiring Type', store=True, required=False)
    # c_classification_level = fields.Selection([('', ''),('rank_file', 'Rank and File'), ('manager', 'Manager'),('individual_contributor', 'Individual Contributor'), ('supervisor', 'Supervisor'), ('director', 'Director')],'Classification/Level', store=True, required=False)
    # sourcing_channel = fields.Char('Sourcing Channel', store=True, required=False)
    # referrer = fields.Char('Referrer', store=True, required=False)
    # c_employment_status = fields.Selection([('', ''),('probationary', 'Probationary'), ('regular', 'Regular'), ('project_based', 'Project-Based')],'Employment Status', store=True, required=False)
    # projected_start_date = fields.Date('Projected Start Date', store=True, required=False)
    # orientation_date = fields.Date('Orientation Date', store=True, required=False)
    # actual_start_date = fields.Date('Actual Start Date', store=True, required=False)
    # residing_within_metro_manila = fields.Char('Residing within Metro Manila?', store=True, required=False)
    # mobile_number = fields.Char('Primary Mobile Number', store=True, compute='_compute_formatted_phone_number', required=False, readonly=False)
    # secondary_formatted_phone_number = fields.Char('Secondary Mobile Number', store=True, required=False)
    # # @api.constrains('mobile_number')
    # # def _check_phone_number_length(self):
    # #     for record in self:
    # #         if record.mobile_number and len(record.mobile_number) != 13:
    # #             raise ValidationError("Primary Mobile Number must be 11 characters.")

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
            

    # email = fields.Char('Email', store=True, required=False)
    # # Green Part Extra
    # complete_name = fields.Char('Complete Name', store=True, compute='_compute_complete_name', required=False)
    # @api.depends('first_name', 'last_name')
    # def _compute_complete_name(self):
    #     for record in self:
    #         if record.first_name and record.last_name:
    #             record.complete_name = record.first_name + ' ' + record.last_name
    #         else:
    #             record.complete_name = False

    # # Client Services Part

    # training_schedule_default_shift = fields.Char('Training Schedule/Default Shift', store=True, required=False)
    # system_requirement = fields.Text('System Requirement', store=True, required=False)
    # instructions_for_it_team = fields.Text('Instructions for IT Team', store=True, required=False)
    # training_poc = fields.Char('Training POC', store=True, required=False)
    # training_poc_contact_information = fields.Char('Training POC Contact Information', store=True, required=False)
    # channel_of_communication = fields.Char('Channel of Communication', store=True, required=False)
    # operations_schedule = fields.Char('Operations Schedule', store=True, required=False)
    # date_of_first_day_of_operations = fields.Date('Date of First Day of Operations', store=True, required=False)
    # direct_supervisor = fields.Char('Direct Supervisor', store=True, required=False)
    # direct_supervisor_contact_information = fields.Char('Direct Supervisor Contact Information', store=True, required=False)
    # working_onsite = fields.Char('Working Onsite?', store=True, required=False)
    # c_company = fields.Selection([('isupport_worldwide', 'iSupport Worldwide'), ('iswerk', 'ISWerk')], 'Company', store=True, required=False)

    # # HR Onboarding Part 1
    # verified_all_information_are_correct = fields.Char('Verified All Information Are Correct', store=True, required=False)
    # medical_completed = fields.Char('Medical Completed', store=True, required=False)
    # id_photo = fields.Char('ID Photo(Yes/No)', store=True, required=False)
    # sss = fields.Char('SSS(Yes/No)', store=True, required=False)
    # tin = fields.Char('TIN(Yes/No)', store=True, required=False)
    # philhealth = fields.Char('PHILHEALTH(Yes/No)', store=True, required=False)
    # pag_ibig = fields.Char('PAG-IBIG(Yes/No)', store=True, required=False)
    # nbi_clearance = fields.Char('NBI Clearance', store=True, required=False)
    # letter_of_undertaking = fields.Char('Letter of Undertaking', store=True, required=False)
    # okay_to_start = fields.Char('Okay to Start?', store=True, required=False)
    # completed_neo = fields.Char('Completed NEO?', store=True, required=False)
    
    # # IT Part
    # pc_ready_for_deployment = fields.Char('PC Ready for Deployment?', store=True, required=False)
    # logins_created = fields.Char('NT Logins Created?', store=True, required=False)
    # isw_hostgator_email_created = fields.Char('ISW Hostgator Email Created?', store=True, required=False)
    # nt_logins_sent_to_employee = fields.Char('NT Logins and ISW Hotgator Email Sent to Employee?', store=True, required=False)
    # signed_accountability_form_received = fields.Char('Signed Accountability Form Received?', store=True, required=False)
    # uid = fields.Char('UID', store=True, required=False)

    # # HR Onboarding Part 2
    # email_equipment_ready_for_pickup_sent = fields.Char('Email (Equipment Ready for pickup) Sent?', store=True, required=False)
    # vaccinated = fields.Char('Vaccinated?', store=True, required=False)
    # projected_nh_report_sent = fields.Char('Projected NH Report Sent?', store=True, required=False)
    # welcome_email_neo_invite = fields.Char('NEO Invite', store=True, required=False)
    
    # # Recruitment Part
    # onboarding_email = fields.Char('Onboarding Email', store=True, required=False)
    
    # # Facilities Part
    # prepared_gatepass_for_pick_up = fields.Char('Prepared Gatepass for Pick Up?', store=True, required=False)
    # pc_released = fields.Char('PC Released?', store=True, required=False)
    # work_set_up_finalized = fields.Char('Work Set Up Finalized?', store=True, required=False)
    # picked_up_by = fields.Char('Picked Up By', store=True, required=False)
    # new_hire_kits_released = fields.Char('New Hire Kits Released', store=True, required=False)

    # # CS Part
    # onboarding_report_sent_to_client = fields.Char('Onboarding Report Sent to Client?', store=True, required=False)

    # # C&B Part
    # mypayroll_approver = fields.Char('MyPayroll Approver', store=True, required=False)

    # # Blank Part
    # status = fields.Char('Status', store=True, required=False)


    