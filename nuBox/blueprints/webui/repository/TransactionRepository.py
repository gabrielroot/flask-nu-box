from datetime import datetime, timedelta
from sqlalchemy import extract
from nuBox.blueprints.webui.utils.OPTransactionEnum import TransactionOperation
from nuBox.ext.database import db, Box as BoxModel, Transaction as TransactionModel, Balance as BalanceModel

class TransactionRepository:
    @staticmethod
    def findMyActivesTransactions(current_user):
        return TransactionModel.query.\
            join(TransactionModel.box, isouter=True).\
            join(TransactionModel.balance, isouter=True).\
            filter(TransactionModel.deleted == False).\
            filter(db.or_(BoxModel.user_id == current_user.id, BalanceModel.user_id == current_user.id)).\
            filter(db.or_(BoxModel.deleted == False, BalanceModel.deleted == False)).\
            order_by(TransactionModel.createdAt.desc())

    @staticmethod
    def sumOfWithdrawsOrDepositsFromBoxes(current_user, operation):
        return db.session.query(db.func.sum(TransactionModel.value)).\
            join(TransactionModel.box, isouter=True).\
            filter(BoxModel.user_id == current_user.id, BoxModel.deleted == False).\
            filter(TransactionModel.operation == operation, TransactionModel.deleted == False).\
            scalar()
    

    @staticmethod
    def countTransactionsInBoxesByWeekDay(current_user):
        today = datetime(datetime.today().year, datetime.today().month, datetime.today().day)
        days_since_sunday = today.weekday() + 1 if today.weekday() != 6 else 0
        past_sunday = today - timedelta(days=days_since_sunday)
        week_days = {}
        for operation in TransactionOperation:
            week_days[operation.name] = []
            for day in range(0, 7):
                count = db.session.query(db.func.COUNT(TransactionModel.id)).\
                    join(TransactionModel.box, isouter=True).\
                    filter(BoxModel.user_id == current_user.id, BoxModel.deleted == False).\
                    filter(TransactionModel.operation == operation.name, TransactionModel.deleted == False).\
                    filter(db.func.DATE(TransactionModel.date) >= past_sunday, extract('dow', TransactionModel.date) == day).\
                    scalar()
                week_days[operation.name].append(count)  
        return week_days