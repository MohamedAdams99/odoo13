from odoo import api, fields, models


class CreateAppointment(models.TransientModel):
    _name = 'create.appointment'
    _description = 'Create Appointment Wizard'

    patient_id = fields.Many2one("hospital.patient", string="Patient")
    appointment_date = fields.Date(string="Appointment Date")

    def print_report(self):
        data = {
            'model' : 'create_appointment',
            'form' : self.read()[0]
        }
        return self.env.ref('clinic.appointment_report').report_action(self, data=data)

    def create_appointment(self):
        vals = {
            'patient_id': self.patient_id.id,
            'appointment_date': self.appointment_date
        }
        self.env['hospital.appointment'].create(vals)

    # def get_data(self):

