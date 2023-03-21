from projetoFlask.ext.database import db
from projetoFlask.ext.database import Box as BoxModel

class BoxRepository:
    @staticmethod
    def findMyActivesBoxes(current_user):
        return BoxModel.query.\
            filter_by(deleted=False, user=current_user).\
            order_by(BoxModel.name)
    
    @staticmethod
    def findOneActiveBox(id, current_user):
        return BoxModel.query.\
            filter_by(id=id, deleted=False, user=current_user).\
            first()
    
    @staticmethod
    def getSumOfValuesInBoxes(current_user):
        return db.session.query(db.func.sum(BoxModel.value)).\
            filter(BoxModel.deleted == False, BoxModel.user == current_user).\
            scalar()
    
    @staticmethod
    def countAllGoalBoxes(current_user):
        return db.session.query(db.func.count(BoxModel.id)).\
            filter(BoxModel.deleted == False, BoxModel.user == current_user, BoxModel.value >= BoxModel.goal).\
            scalar()