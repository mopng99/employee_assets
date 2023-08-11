# -*- coding: utf-8 -*-

from odoo import models, fields, _
from odoo.exceptions import ValidationError


class HrDepartureWizard(models.TransientModel):
    _inherit = 'hr.departure.wizard'

    def action_register_departure(self):
        print(self.employee_id)
        num_company_assets = self.env['company.assets'].search_count([('employee_id', '=', self.employee_id.id), ('state', '!=', 'returned')])
        print(num_company_assets)
        if num_company_assets == 0:
            employee = self.employee_id
            if self.env.context.get('toggle_active', False) and employee.active:
                employee.with_context(no_wizard=True).toggle_active()
            employee.departure_reason_id = self.departure_reason_id
            employee.departure_description = self.departure_description
            employee.departure_date = self.departure_date

            if self.archive_private_address:
                # ignore contact links to internal users
                private_address = employee.address_home_id
                if private_address and private_address.active and not self.env['res.users'].search(
                        [('partner_id', '=', private_address.id)]):
                    private_address.sudo().toggle_active()
        else:
            raise ValidationError(_('The employee %s has assets that have not been returned' % self.employee_id.name))



