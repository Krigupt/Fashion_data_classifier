from fashion_classifier import db,login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(db.Model,UserMixin):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)


    def __repr__(self):
        return f"User('{self.username}','{self.email}')"




class ClothingData(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    cloth_type = db.Column(db.String(50))
    gender_type = db.Column(db.String(50))
    size_type = db.Column(db.String(50))
    color = db.Column(db.String(50))
    image_file = db.Column(db.String(20), nullable=False, default='default.jpeg')

    def __repr__(self):
        return f"User('{self.cloth_type}','{self.gender_typ}','{self.size_type}','{self.color}')"