from odoo import api, fields, models


class HospitalSettings(models.TransientModel):
    _name = 'hospital.settings'
    _inherit = 'res.config.settings'

    note = fields.Char(string='Default Note')

    def set_values(self):
        res = super(HospitalSettings, self).set_values()
        self.env['ir.config_parameter'].set_param('clinic.notes', self.note)
        return res

    @api.model
    def get_values(self):
        res = super(HospitalSettings, self).set_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        notes = ICPSudo.get_param('clinic.note')
        res.update(note=notes)
        return res
