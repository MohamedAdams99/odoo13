from odoo import api, fields, models


class HospitalDoctor(models.Model):
    _name = 'hospital.doctor'
    _description = 'Hospital Doctors'

    name = fields.Char(string="Name")
    gender = fields.Selection(string="Gender", selection=[('male', 'Male'), ('female', 'Female')],
                              required=True, default="male")
    doctor = fields.Many2one('res.users', string="Doctor", required=False)
