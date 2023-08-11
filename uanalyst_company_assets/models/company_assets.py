# -*- coding: utf-8 -*-
from odoo import models, fields, _, api
from odoo.exceptions import ValidationError

from odoo.exceptions import UserError


class CompanyAssets(models.Model):
    _name = 'company.assets'
    _description = 'Company Assets'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'product_id'

    reference = fields.Char(default="NEW", compute="_compute_ref")
    reference_received = fields.Many2one('stock.picking', string="Reference Received")
    reference_returned = fields.Many2one('stock.picking', string="Reference Returned")
    employee_id = fields.Many2one('hr.employee', string='Employee', required=True, tracking=True)
    product_id = fields.Many2one('product.template', string='Product', required=True, tracking=True)
    quantity = fields.Integer(string='Quantity Demand', required=True, tracking=True)
    state = fields.Selection([
        ('requested', 'Requested'),
        ('received', 'Received'),
        ('returned', 'Returned')]
        , default="requested", string="Status", tracking=True)
    state_received = fields.Selection([
        ('draft', 'Draft'),
        ('waiting', 'Waiting Another Operation'),
        ('confirmed', 'Waiting'),
        ('assigned', 'Ready'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')]
        , default="draft", string="Status Received", tracking=True, readonly=True)
    state_returned = fields.Selection([
        ('draft', 'Draft'),
        ('waiting', 'Waiting Another Operation'),
        ('confirmed', 'Waiting'),
        ('assigned', 'Ready'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')]
        , default="draft", string="Status Returned", tracking=True, readonly=True)
    receiving_date = fields.Datetime(tracking=True)
    returned_date = fields.Datetime(tracking=True)
    operation_type_id = fields.Many2one('stock.picking.type', string='Operation Type', required=True, tracking=True)
    analytic_distribution = fields.Json(store=True, tracking=True)
    analytic_precision = fields.Integer(
        store=False,
        default=lambda self: self.env['decimal.precision'].precision_get("Percentage Analytic"),
    )

    def unlink(self):
        for rec in self:
            if rec.state != 'requested':
                raise ValidationError(_('You can delete asset state is requested only'))
        return super(CompanyAssets, self).unlink()

    def _compute_ref(self):
        self.reference = self.product_id.name

    def action_confirm(self):

        for rec in self:
            stock_quant_obj = self.env['stock.quant'].search(
                [('location_id', '=', rec.operation_type_id.default_location_src_id.id), ('product_id', '=', rec.product_id.product_variant_id.id)])
            if rec.quantity <= 0:
                raise UserError('Please Enter The Quantity')
            if stock_quant_obj.quantity < rec.quantity:
                raise UserError('The Quantity Free For %s Is %s' % (rec.product_id.product_variant_id.name, stock_quant_obj.quantity))
            for contract_id in rec.employee_id.related_contact_ids:
                rec.ensure_one()
                contrac_id = contract_id

            record_obj = self.env['stock.picking'].create(
                {
                    'partner_id': contrac_id.id,
                    'scheduled_date': rec.receiving_date,
                    'state': 'waiting',
                    'picking_type_id': rec.operation_type_id.id,
                    'location_id': rec.operation_type_id.default_location_src_id.id,
                    'location_dest_id': rec.operation_type_id.default_location_dest_id.id,
                    'move_ids_without_package': [
                        ({
                            'name': 'Stock Transfer',
                            'product_id': rec.product_id.product_variant_id.id,
                            'product_uom_qty': rec.quantity,
                            'location_id': rec.operation_type_id.default_location_src_id.id,
                            'location_dest_id': rec.operation_type_id.default_location_dest_id.id,
                        })
                    ],
                }
            )
            rec.reference_received = record_obj.id
            record_obj.action_confirm()
            rec.state = 'received'
            # rec.receiving_date = fields.Date.today()
            rec.product_id.status = 'received'
            rec.product_id.employee_id = rec.employee_id

    def action_return(self):
        for rec in self:
            for contract_id in rec.employee_id.related_contact_ids:
                rec.ensure_one()
                contrac_id = contract_id
            return_oper_type_id = rec.operation_type_id.return_picking_type_id
            record_obj = self.env['stock.picking'].create(
                {
                    'partner_id': contrac_id.id,
                    'scheduled_date': rec.returned_date,
                    'state': 'waiting',
                    'picking_type_id': return_oper_type_id.id,
                    'location_id': return_oper_type_id.default_location_src_id.id,
                    'location_dest_id': return_oper_type_id.default_location_dest_id.id,
                    'move_ids_without_package': [
                        ({
                            'name': 'Stock Transfer',
                            'product_id': rec.product_id.product_variant_id.id,
                            'product_uom_qty': rec.quantity,
                            'location_id': return_oper_type_id.default_location_src_id.id,
                            'location_dest_id': return_oper_type_id.default_location_dest_id.id,
                        })
                    ],
                }
            )
            rec.reference_returned = record_obj.id
            record_obj.action_confirm()
            rec.state = 'returned'
            # rec.returned_date = fields.Date.today()
            rec.product_id.status = 'returned'
            rec.product_id.employee_id = False

