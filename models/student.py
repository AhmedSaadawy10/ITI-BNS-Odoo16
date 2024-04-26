from odoo import models, fields, api, exceptions


class Student(models.Model):
    _name = "iti.student"

    name = fields.Char(required=True)
    email = fields.Char()
    birthdate = fields.Date()
    salary = fields.Float()
    tax = fields.Float(compute="_compute_tax", store=True)
    address = fields.Text()
    gender = fields.Selection(
        [
            ('male', 'Male'),
            ('female', 'Female'),
        ], default='mail',
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
    state = fields.Selection([
        ('applied', "Applied"),
        ('first', "First Interview"),
        ('second', "Second Interview"),
        ('passed', "Passed"),
        ('rejected', "Rejected"),
    ], default='applied')

    @api.depends('salary')
    def _compute_tax(self):
        for rec in self:
            rec.tax = rec.salary * 0.15

    """
    Checks if the track capacity is exceeded by the number of students in the track.

    :param self: The current object.
    :raises: `ValidationError` if the track capacity is exceeded.
    """
    @api.constrains('track_id')
    def _check_track_capacity(self):
        track_count = len(self.track_id.student_ids)
        track_capacity = self.track_id.capacity
        if track_count > track_capacity:
            raise exceptions.ValidationError('This track is full')

    """
    Check the validity of the salary field for the current record.

    This function is a constrain method that is triggered whenever the salary field is modified.
    It checks if the salary is negative or greater than 1000 and raises a ValidationError if it is.

    Raises:
        ValidationError: If the salary is negative or greater than 1000.

    Returns:
        None
    """
    @api.constrains('salary')
    def _check_salary(self):
        if self.salary < 0:
            raise exceptions.ValidationError('Salary cannot be negative')
        elif self.salary > 10000:
            raise exceptions.ValidationError('Salary cannot be greater than 10000')

    """
    Create a new student record with the given values.

    Args:
        vals (dict): A dictionary containing the values to set on the new student record.

    Returns:
        Record: The newly created student record.

    Raises:
        None

    Description:
        This function creates a new student record by calling the `create` method of the superclass.
        It then splits the `name` field of the new student record and constructs the `email` field by concatenating
        the first letter of the first name and the last name, 
        followed by "@gmail.com". Finally, it returns the newly created student record.

    Example:
        >>> student
    """
    @api.model
    def create(self, vals):
        new_student = super().create(vals)
        new_split = new_student.name.split()
        new_student.email = f"{new_split[0][0]}{new_split[1]}@gmail.com"
        # if this email is already existing, it will raise an error
        existing_student_email = self.search([('email', '=', new_student.email)], limit=1)
        if existing_student_email:
            raise exceptions.ValidationError('This email is already taken by another student')
        return new_student

    """
    Writes the given values to the model.

    :param vals: A dictionary of field names and their new values.
    :type vals: dict
    """

    def write(self, vals):
        if 'name' in vals:
            new_split = vals['name'].split()
            vals['email'] = f"{new_split[0][0]}{new_split[1]}@gmail.com"
        super().write(vals)

        """
        Unlinks the records from the model.

        This method iterates over each record in the current model 
        and checks if the state of the record is either 'passed' or 'rejected'. 
        If the state is either of these values,
        a UserError is raised with the message "You can't delete a passed or rejected student".
        Otherwise, the records are unlinked using the super().unlink() method.

        Parameters:
            self (Model): The current model instance.

        Raises:
            UserError: If the state of any record is 'passed' or 'rejected'.

        Returns:
            None
        """

    def unlink(self):
        for record in self:
            if record.state in ['passed', 'rejected']:
                raise exceptions.UserError("You can't delete a passed or rejected student")

        super().unlink()

    def change_state(self):
        if self.state == 'applied':
            self.state = 'first'
        elif self.state == 'first':
            self.state = 'second'
        elif self.state in ['passed', 'rejected']:
            self.state = 'applied'

    def set_passed(self):
        self.state = 'passed'

    def set_rejected(self):
        self.state = 'rejected'

    """
    This function is called when the 'gender' field is changed. 
    It updates the salary based on the gender value. 
    It returns a dictionary containing a warning message and a domain for the field.
    :return: dictionary containing a warning message and a domain
    :rtype: dict
    """

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
