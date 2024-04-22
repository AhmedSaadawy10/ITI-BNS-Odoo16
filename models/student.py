from odoo import models, fields, api


class Student(models.Model):
    _name = "iti.student"

    name = fields.Char(required=True)
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
    track_id = fields.Many2one("iti.track")
    track_capacity = fields.Integer(related="track_id.capacity")
    skills_ids = fields.Many2many("iti.skill")
    grade_ids = fields.One2many("student.course.line", "student_id")

    @api.onchange("gender")
    def on_change_gender(self):
        domain = {'track_id': []}
        if self.gender and self.gender == 'male':
            domain = {'track_id': [('is_open', '=', True)]}
            self.salary = 5000
        else:
            self.salary = 3000
        return {
            "warning": {
                "title": "Note",
                "message": "the salary changed based on the gender"
            },
            "domain": domain

        }


class StudentSkill(models.Model):
    _name = "student.skill.line"

    student_id = fields.Many2one("iti.student")
    skill_id = fields.Many2one("iti.skill")
    grade = fields.Selection([
        ('excellent', "Excellent"),
        ('very good', "Very Good"),
        ('good', "Good"),
        ('fair', "Fair"),
        ('bad', "Bad"),
    ])


class StudentCourseGrade(models.Model):
    _name = "student.course.line"

    student_id = fields.Many2one("iti.student")
    course_id = fields.Many2one("iti.course")
    grade = fields.Selection([
        ('excellent', "Excellent"),
        ('very good', "Very Good"),
        ('good', "Good"),
        ('fair', "Fair"),
        ('bad', "Bad"),
    ])


