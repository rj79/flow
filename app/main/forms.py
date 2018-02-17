from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, EqualTo
from flask_babel import _, lazy_gettext as _l
from app.model import User

class CreateIssueForm(FlaskForm):
    project_id = SelectField(_l('Project'), coerce=int)
    issue_type_id = SelectField(_l('Issue type'), coerce=int)
    title = StringField(_l('Title'), validators=[DataRequired()])
    description = TextAreaField(_l('Description'), validators=[])
    submit = SubmitField(_('Create'))
