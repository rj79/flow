from flask_wtf import FlaskForm
from wtforms import StringField, DateField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, EqualTo
from flask_babel import _, lazy_gettext as _l

class CreateReleaseForm(FlaskForm):
    name = StringField(_l('Name'), validators=[DataRequired()])
    date = DateField(_l('Release date'), validators=[DataRequired()])
    submit = SubmitField(_('Create'))
