from projetoFlask.ext.database import db
from projetoFlask.ext.database import Box as BoxModel, Balance as BalanceModel, Transaction as TransactionModel

class BalanceRepository:  
    @staticmethod
    def getAllSummation(current_user):
        in_boxes = db.session.query(db.func.sum(BoxModel.value)).\
            filter(BoxModel.user == current_user, BoxModel.deleted == False).\
            scalar()
    
        in_balances = db.session.query(db.func.sum(BalanceModel.total)).\
            filter(BalanceModel.user == current_user, BalanceModel.deleted == False).\
            scalar()

        return in_boxes + in_balances
