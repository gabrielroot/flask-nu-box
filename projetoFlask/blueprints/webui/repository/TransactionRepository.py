from projetoFlask.ext.database import Box as BoxModel, Transaction as TransactionModel, Balance as BalanceModel
from projetoFlask.ext.database import db

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
