from flask import Blueprint

from .views import boxView, indexView, profileView, transactionView

bp = Blueprint(
    "webui",
    __name__,
    template_folder="templates",
    url_prefix="/",
    static_folder='static',
    static_url_path='/static/webui'
)

bp.add_url_rule('/', view_func=indexView.index)

bp.add_url_rule('/my-boxes', view_func=boxView.myBoxes)
bp.add_url_rule('/my-boxes/new', view_func=boxView.newBox,
                methods=['GET', 'POST']
                )
bp.add_url_rule('/my-boxes/<int:id>/edit', view_func=boxView.editBox,
                methods=['GET', 'POST']
                )
bp.add_url_rule('/my-boxes/<int:id>/delete', view_func=boxView.deleteBox,
                methods=['GET']
                )

bp.add_url_rule('/my-transactions', view_func=transactionView.myTransactions,
                methods=['GET']
                )
bp.add_url_rule('/my-boxes/<int:box_id>/deposit-withdraw',
                view_func=transactionView.newTransaction,
                methods=['GET', 'POST']
                )

bp.add_url_rule('/profile', view_func=profileView.profile)
bp.add_url_rule('/profile/deposit-withdraw',
                view_func=transactionView.newBalanceTransaction,
                methods=['GET', 'POST']
                )
