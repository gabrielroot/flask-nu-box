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
