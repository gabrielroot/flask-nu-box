from flask import Blueprint
from .views import *

bp = Blueprint("webui", __name__, template_folder="templates",
    url_prefix="/", static_folder='static', static_url_path='/static/webui'
)

bp.add_url_rule('/', view_func=index)

bp.add_url_rule('/my-boxes', view_func=myBoxes)
bp.add_url_rule('/my-boxes/new', view_func=newBox, methods=['GET', 'POST'])
bp.add_url_rule('/my-boxes/<int:id>/edit', view_func=editBox, methods=['GET', 'POST'])
bp.add_url_rule('/my-boxes/<int:id>/delete', view_func=deleteBox, methods=['GET'])

bp.add_url_rule('/my-transactions', view_func=myTransactions, methods=['GET'])
bp.add_url_rule('/my-boxes/<int:box_id>/deposit-withdraw', view_func=newTransaction, methods=['GET', 'POST'])

bp.add_url_rule('/profile', view_func=profile)
bp.add_url_rule('/profile/deposit-withdraw', view_func=newBalanceTransaction, methods=['GET', 'POST'])