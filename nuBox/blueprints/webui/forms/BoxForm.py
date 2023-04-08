from wtforms import HiddenField, StringField, IntegerField, TextAreaField
from flask_wtf import Form
from wtforms.validators import Length, DataRequired


class BoxCreate(Form):
    id = HiddenField()
    name = StringField(
        'Nome',
        validators=[DataRequired(), Length(min=4, max=20)],
        render_kw={"placeholder": "Informe o nome da caixinha"}
    )
    goal = IntegerField(
        'Meta', validators=[DataRequired()],
        render_kw={"placeholder": "Pense em uma meta..."}
    )
    value = IntegerField('Saldo', render_kw={"disabled": "true"})
    description = TextAreaField(
        'Descrição',
        render_kw={"placeholder": "Eu criei essa caixinha por que..."}
    )
