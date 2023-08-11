# -*- coding: utf-8 -*-

from odoo import models, fields, _, api


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.constrains('state')
    def _compute_status_company_assets(self):
        for rec in self:
            received_obj = self.env['company.assets'].search([('reference_received', '=', rec.id)])
            return_obj = self.env['company.assets'].search([('reference_returned', '=', rec.id)])
            if received_obj:
                received_obj.state_received = rec.state
            if return_obj:
                return_obj.state_returned = rec.state
