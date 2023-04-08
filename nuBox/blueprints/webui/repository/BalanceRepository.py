from operator import is_not

from nuBox.ext.database import Box as BoxModel
from nuBox.ext.database import Balance as BalanceModel
from nuBox.ext.database import db


class BalanceRepository:
    @staticmethod
    def getAllSummation(current_user):
        in_boxes = db.session.query(db.func.sum(BoxModel.value)).\
            filter(BoxModel.user == current_user, is_not(BoxModel.deleted, False)).\
            scalar()

        in_balances = db.session.query(db.func.sum(BalanceModel.total)).\
            filter(BalanceModel.user == current_user, is_not(BalanceModel.deleted, True)).\
            scalar()

        in_boxes = in_boxes if in_boxes else 0
        in_balances = in_balances if in_balances else 0

        return in_boxes + in_balances
