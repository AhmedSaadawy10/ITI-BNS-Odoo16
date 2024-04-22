from odoo import models, fields


class Skill(models.Model):
    _name = "iti.skill"

    name = fields.Char()
