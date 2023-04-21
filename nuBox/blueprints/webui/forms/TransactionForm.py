from wtforms import RadioField, HiddenField, IntegerField, TextAreaField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired

from nuBox.blueprints.webui.utils.OPTransactionEnum import TransactionOperation


class TransactionCreate(FlaskForm):
    id = HiddenField()
    operation = RadioField(
        'Operação',
        choices=[
            (
                TransactionOperation.DEPOSIT.name,
                TransactionOperation.DEPOSIT.value
            ),
            (
                TransactionOperation.WITHDRAW.name,
                TransactionOperation.WITHDRAW.value
            )
        ],
        default=TransactionOperation.DEPOSIT.name
    )
    value = IntegerField(
        'Valor',
        validators=[DataRequired()],
        render_kw={"placeholder": "informe o valor"}
    )
    description = TextAreaField(
        'Descrição',
        render_kw={"placeholder": "Fale um pouco do motivo"}
    )
