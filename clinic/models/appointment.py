# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class HospitalAppointment(models.Model):
    _name = 'hospital.appointment'
    _inherit = ['mail.thread.cc', 'mail.activity.mixin']
    _description = 'Appointment Record'
    _order = 'id desc'

    name = fields.Char(string='Appointment ID', required=True, copy=False,
                       readonly=True, index=True, default=lambda self: _('New'))
    patient_id = fields.Many2one('hospital.patient', string='Patient', required=True)
    patient_age = fields.Integer(string='Age', related='patient_id.patient_age')
    total_amount = fields.Float(string="Total Amount")
    notes = fields.Text(string='Registration Note')
    doctor_note = fields.Text(string='Doctor Note')
    doctor_id = fields.Many2one("hospital.doctor", string="Doctor")
    appointment_lines = fields.One2many('hospital.appointment.lines', 'appointment_id', string="Appointment Lines")
    pharmacy_note = fields.Text(string='Pharmacy Note')
    partner_id = fields.Many2one("res.partner", string="Customer")
    order_id = fields.Many2one("sale.order", string="Sale Order")
    appointment_date = fields.Date(string='Date', required=True)
    appointment_datetime = fields.Datetime(string="Date Time")
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirm'),
                              ('done', 'Done'), ('cancel', 'Cancel')], string='Status', readonly=True, default='draft')

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('hospital.appointment.sequence') or _('New')
        result = super(HospitalAppointment, self).create(vals)
        return result

    def action_confirm(self):
        for rec in self:
            rec.state = 'confirm'

    def action_done(self):
        for rec in self:
            rec.state = 'done'
            return {
                'effect': {
                    'fadeout': 'slow',
                    'message' : 'Appointment Done ..',
                    'type' : 'rainbow_man'
                }
            }

    def delete_lines(self):
        for rec in self:
            rec.appointment_lines = [(5, 0, 0)]

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        for rec in self:
            return {'domain': {'order_id': [('partner_id', '=', rec.partner_id.id)]}}


class HospitalAppointmentLines(models.Model):
    _name = 'hospital.appointment.lines'
    _description = 'Hospital Appointment Lines'

    product_id = fields.Many2one('product.product', string='Medicine')
    product_qty = fields.Integer(string="Quantity")
    appointment_id = fields.Many2one('hospital.appointment', string="Appointment ID")


