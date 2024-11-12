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
    _name = 'tags'
    _description = 'Tags'
    _rec_name = 'tags'

    def _get_default_color(self):
        return randint(1, 11)

    tags = fields.Char('Tags', store=True)
    color = fields.Integer('Color', default=_get_default_color, store=True)