from odoo import models,fields


class Course(models.Model):
    _name = "iti.course"

    name = fields.Char()
