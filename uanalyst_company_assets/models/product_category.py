# -*- coding: utf-8 -*-

from odoo import api, models, fields, _


class ProductCategory(models.Model):
    _inherit = 'product.category'

    default_code_category = fields.Char('Code Category', translate=True, store=True)
    default_code_num = fields.Integer('Code', store=True)


