from projetoFlask.ext.database import db
from projetoFlask.ext.database import Box as BoxModel, Balance as BalanceModel

class BalanceRepository:
    @staticmethod
    def getAllSummation(current_user):
        return db.session.query(db.func.sum(BoxModel.value + BalanceModel.total)).\
            filter(BoxModel.deleted == False, BoxModel.user == current_user).\
            filter(BalanceModel.user == current_user).\
            scalar()
