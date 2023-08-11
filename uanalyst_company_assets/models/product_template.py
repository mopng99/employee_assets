# -*- coding: utf-8 -*-

from odoo import api, models, fields, _
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    uanalyst_company_asset = fields.Boolean(string="Company Assets", default=True)
    status = fields.Selection([
        ('requested', 'Requested'),
        ('received', 'Received'),
        ('returned', 'Returned')]
        , default="requested", string="status", tracking=True)
    employee_id = fields.Many2one('hr.employee', string='Received By', tracking=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            default_code = self.env['product.category'].browse(vals['categ_id']).default_code_category
            default_code_num = self.env['product.category'].browse(vals['categ_id']).default_code_num
            if default_code:
                if not vals.get('default_code', _('New')):
                    if self.env['product.category'].browse(vals['categ_id']).default_code_num < 10:
                        vals['default_code'] = default_code + " - 0000" + str(default_code_num)
                    if 9 < self.env['product.category'].browse(vals['categ_id']).default_code_num:
                        vals['default_code'] = default_code + " - 000" + str(default_code_num)
                    if 99 < self.env['product.category'].browse(vals['categ_id']).default_code_num:
                        vals['default_code'] = default_code + " - 00" + str(default_code_num)
                    if 999 < self.env['product.category'].browse(vals['categ_id']).default_code_num:
                        vals['default_code'] = default_code + " - 0" + str(default_code_num)
                    self.env['product.category'].browse(vals['categ_id']).default_code_num += 1
            else:
                raise ValidationError(_("This product category has not default category code."))
        return super(ProductTemplate, self).create(vals_list)

    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        default_code = self.categ_id.default_code_category
        default_code_num = self.categ_id.default_code_num
        default = dict(default or {})
        if default_code:
            if self.env['product.category'].browse(self.categ_id.id).default_code_num < 10:
                default['default_code'] = default_code + " - 0000" + str(default_code_num)
            if 9 < self.env['product.category'].browse(self.categ_id.id).default_code_num:
                default['default_code'] = default_code + " - 000" + str(default_code_num)
            if 99 < self.env['product.category'].browse(self.categ_id.id).default_code_num:
                default['default_code'] = default_code + " - 00" + str(default_code_num)
            if 999 < self.env['product.category'].browse(self.categ_id.id).default_code_num:
                default['default_code'] = default_code + " - 0" + str(default_code_num)
            self.env['product.category'].browse(self.categ_id.id).default_code_num += 1
        else:
            raise ValidationError(_("This product category has not default category code."))
        return super(ProductTemplate, self).copy(default)





