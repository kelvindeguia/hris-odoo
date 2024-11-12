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

class Account(models.Model):
    _name = 'accounts'
    _description = 'Accounts in ISW'
    _rec_name = 'department_account'

    active = fields.Boolean('Active', store=True, default=True)
    department_account = fields.Char('Department/Account', store=True)
    company = fields.Char('Company', store=True)