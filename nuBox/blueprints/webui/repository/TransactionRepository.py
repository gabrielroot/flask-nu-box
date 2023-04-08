from datetime import datetime
from operator import is_not

from sqlalchemy import extract

from nuBox.ext.database import Box as BoxModel
from nuBox.ext.database import Balance as BalanceModel
from nuBox.ext.database import Transaction as TransactionModel
from nuBox.ext.database import db
from nuBox.blueprints.webui.utils.OPTransactionEnum import TransactionOperation


class TransactionRepository:
    @staticmethod
    def findMyActivesTransactions(current_user):
        return TransactionModel.query.\
            join(TransactionModel.box, isouter=True).\
            join(TransactionModel.balance, isouter=True).\
            filter(
                is_not(TransactionModel.deleted, True),
                db.or_(BoxModel.user_id == current_user.id, BalanceModel.user_id == current_user.id),
                db.or_(is_not(BoxModel.deleted, True), is_not(BalanceModel.deleted, True))
            ).\
            order_by(TransactionModel.createdAt.desc())

    @staticmethod
    def sumOfWithdrawsOrDepositsFromBoxes(current_user, operation):
        return db.session.query(db.func.sum(TransactionModel.value)).\
            join(TransactionModel.box, isouter=True).\
            filter(
                BoxModel.user_id == current_user.id,
                is_not(BoxModel.deleted, True),
                TransactionModel.operation == operation,
                is_not(TransactionModel.deleted, True)
        ).scalar()

    @staticmethod
    def countTransactionsInBoxesByWeekDay(current_user):
        january = datetime(datetime.today().year, 1, 1)

        months = {}
        for operation in TransactionOperation:
            months[operation.name] = []
            for month in range(1, 13):
                count = db.session.query(db.func.COUNT(TransactionModel.id)).\
                    join(TransactionModel.box, isouter=True).\
                    filter(
                        BoxModel.user_id == current_user.id,
                        is_not(BoxModel.deleted, True),
                        TransactionModel.operation == operation.name,
                        is_not(TransactionModel.deleted, True),
                        db.func.DATE(TransactionModel.date) >= january,
                        extract('MONTH', TransactionModel.date) == month
                ).scalar()
                months[operation.name].append(count)
        return months
