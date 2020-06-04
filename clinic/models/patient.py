# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def create(self, vals_list):
        res = super(ResPartner, self).create(vals_list)
        print('//////////')
        return res


class SaleOrederInherit(models.Model):
    _inherit = 'sale.order'

    patient_name = fields.Char(string='Patient Name')


class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _inherit = ['mail.thread.cc', 'mail.activity.mixin']
    _description = 'Patient Record'
    _rec_name = 'patient_name'

    name = fields.Char(string='Test')
    name_seq = fields.Char(string='Patient ID', required=True, copy=False,
                           readonly=True, index=True, default=lambda self: _('New'))
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], default='male', string='Gender')
    doctor_gender = fields.Selection([('male', 'Male'), ('female', 'Female')], default='male', string='Doctor Gender')
    age_group = fields.Selection([('major', 'Major'), ('minor', 'Minor')], string='Age Group')
    patient_name = fields.Char(string='Name', required=True)
    doctor_id = fields.Many2one('hospital.doctor', string="Doctor", required=False)
    patient_age = fields.Integer(string='Age', track_visiabilty='always')
    patient_name_upper = fields.Char(compute="_compute_upper_name", inverse='_inverse_upper_name')
    email = fields.Char(string="Email")
    notes = fields.Text(string='Registration Note')
    image = fields.Binary(string='Image', attatchment=True)
    test = fields.Char(string='Test', attatchment=True)
    phone = fields.Integer(string='Phone')
    appointment_count = fields.Integer(string='Appointment', compute='get_appointment_count')
    active = fields.Boolean(string='Active', default=True)
    user_id = fields.Many2one("res.users", string="PRO", )

    @api.depends('patient_name')
    def _compute_upper_name(self):
        for rec in self:
            rec.patient_name_upper = rec.patient_name.upper() if rec.patient_name else False

    def _inverse_upper_name(self):
        for rec in self:
            rec.patient_name = rec.patient_name_upper.lower() if rec.patient_name_upper else False

    def name_get(self):
        res = []
        for field in self:
            res.append((field.id, '%s - %s' % (field.name_seq, field.patient_name)))
        return res
    ### function is work but get erorr when i click on menu patients
    # @api.depends('patient_age')
    # def set_age_group(self):
    #     for rec in self:
    #         if rec.patient_age < 18:
    #             rec.patient_group = 'minor'
    #         else:
    #             rec.patient_group = 'major'

    @api.onchange('doctor_id')
    def set_doctor_gender(self):
        for rec in self:
            if rec.doctor_id:
                rec.doctor_gender = rec.doctor_id.gender

    @api.constrains('patient_age')
    def check_age(self):
        for rec in self:
            if rec.patient_age <= 5:
                raise ValidationError(_('The Age Must Be Grater Than 5'))

    @api.model
    def create(self, vals):
        if vals.get('name_seq', _('New')) == _('New'):
            vals['name_seq'] = self.env['ir.sequence'].next_by_code('hospital.patient.sequence') or _('New')
        result = super(HospitalPatient, self).create(vals)
        return result

    def open_patient_appointments(self):
        return {
            'name': _('Appointments'),
            'domain': [('patient_id', '=', self.id)],
            'res_model': 'hospital.appointment',
            'view_id': False,
            'type': 'ir.actions.act_window'
        }

    def get_appointment_count(self):
        count = self.env['hospital.appointment'].search_count([('patient_id', '=', self.id)])
        self.appointment_count = count

    def action_send_card(self):
        template_id = self.env.ref('clinic.patient_card_email_template').id
        template = self.env['mail.template'].browse(template_id)
        template.send_mail(self.id, force_send=True)

    def test_cron_job(self):
        print('//////////////')
