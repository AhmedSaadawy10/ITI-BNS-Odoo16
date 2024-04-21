from odoo import models, fields


class Student(models.Model):
    _name = "iti.student"

    name = fields.Char()
    birthdate = fields.Date()
    salary = fields.Float()
    address = fields.Text()
    gender = fields.Selection(
        [
            ('male', 'Male'),
            ('female', 'Female'),
        ]
    )
    accepted = fields.Boolean()
    level = fields.Integer()
    image = fields.Binary()
    cv = fields.Html()
    login_time = fields.Datetime()
