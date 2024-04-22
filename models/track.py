from odoo import models, fields


class Track(models.Model):
    _name = "iti.track"

    name = fields.Char(string="Name")
    is_open = fields.Boolean(string="Is open")
    capacity = fields.Integer()
    student_ids = fields.One2many("iti.student", "track_id")

