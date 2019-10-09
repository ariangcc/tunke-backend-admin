from app import db 
class AddUpdateDelete():
    def add(self, resource):
        db.session.add(resource)
    
    def update(self):
        pass
    
    def delete(self, resource):
        db.session.delete(resource)
        return db.session.commit()