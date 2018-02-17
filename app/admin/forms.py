from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, DateField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, EqualTo
from flask_babel import _, lazy_gettext as _l
from wtforms.fields.html5 import DateField as DatePickerField

class CreateProjectForm(FlaskForm):
    key = StringField(_l('Key'), validators=[DataRequired()])
    name = StringField(_l('Name'), validators=[DataRequired()])
    submit = SubmitField(_('Create'))

class CreateReleaseForm(FlaskForm):
    project_id = SelectField('Project', coerce=int)
    name = StringField(_l('Name'), validators=[DataRequired()])
    release_date = DateField(_l('Release date'), format='%Y%m%d', validators=[DataRequired()])
    submit = SubmitField(_('Create'))
