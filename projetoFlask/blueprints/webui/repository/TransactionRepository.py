from projetoFlask.ext.database import db
from projetoFlask.ext.database import Box as BoxModel, Transaction as TransactionModel, Balance as BalanceModel

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