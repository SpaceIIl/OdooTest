from odoo import models, fields, api
from datetime import date


class ResPartner(models.Model):
    _inherit = 'res.partner'

    birthdate = fields.Date(string="Date of Birth")
    personal_id = fields.Char(string="Personal ID")
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')
    ], string="Gender")

    age = fields.Integer(string="Age", compute="_compute_age", store=True)

    INVALID_PERSONAL_ID_WARNING = {
        'warning': {
            'title': "Invalid Personal ID",
            'message': "Please enter a valid Personal ID in the format RRMMDD/XXXX."
        }
    }

    @api.depends('birthdate')
    def _compute_age(self):
        for record in self:
            if record.birthdate:
                today = date.today()
                age = today.year - record.birthdate.year - (
                        (today.month, today.day) < (record.birthdate.month, record.birthdate.day))
                if age < 0:
                    return self.INVALID_PERSONAL_ID_WARNING
                record.age = age
            else:
                record.age = 0

    def _validate_personal_id(self, personal_id):
        # Remove any slash and ensure the ID has 9 or 10 digits only
        personal_id = personal_id.replace("/", "")
        if not personal_id.isdigit() or len(personal_id) not in [9, 10]:
            return False

        # Check for valid date based on YYMMDD
        year = int(personal_id[:2])
        month = int(personal_id[2:4])
        day = int(personal_id[4:6])

        # Adjust month for gender and validate month range
        if month > 50:
            month -= 50
        if not (1 <= month <= 12):
            return False

        # Determine the century
        if len(personal_id) == 9 or year >= 54:
            full_year = 1900 + year  # IDs issued before 1954 are in the 1900s
        else:
            full_year = 2000 + year  # Otherwise, they are in the 2000s

        # Validate the date itself
        try:
            date(full_year, month, day)
        except ValueError:
            return False

        # If 10 digits, validate the control digit
        if len(personal_id) == 10 and int(personal_id) % 11 != 0:
            return False

        return True

    def _calculate_birthdate_and_gender(self, personal_id):
        personal_id = personal_id.replace("/", "")

        # Validate the personal ID
        if not self._validate_personal_id(personal_id):
            return None, None, self.INVALID_PERSONAL_ID_WARNING

        # Extract and calculate birthdate and gender
        year = int(personal_id[:2])
        month = int(personal_id[2:4])
        day = int(personal_id[4:6])

        gender = 'male'
        if month > 50:
            month -= 50
            gender = 'female'

        # Determine the century
        if len(personal_id) == 9 or year >= 54:
            full_year = 1900 + year
        else:
            full_year = 2000 + year

        birthdate = date(full_year, month, day)

        return birthdate, gender, None


    @api.onchange('personal_id')
    def _onchange_personal_id(self):
        for record in self:
            if record.personal_id:
                birthdate, gender, warning = self._calculate_birthdate_and_gender(record.personal_id)
                if warning:
                    return warning
                record.birthdate = birthdate
                record.gender = gender
                record._compute_age()