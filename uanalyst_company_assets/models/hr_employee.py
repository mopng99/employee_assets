# -*- coding: utf-8 -*-

from odoo import models, fields, _


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    uanalyst_num_company_assets = fields.Integer(string="Company Assets", compute="_compute_number_company_assets")

    def open_company_asset_form(self):
        view = {
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'company.assets',
            'name': _('Company Assets'),
            'domain': "[('employee_id','=',%s)]" % self.id,
            'view_type': 'tree,form',
            'context': {
                'default_employee_id': self.id,
            }
        }
        return view

    def _compute_number_company_assets(self):
        for rec in self:
            rec.uanalyst_num_company_assets += rec.env['company.assets'].search_count([('employee_id', '=', rec.id)])
