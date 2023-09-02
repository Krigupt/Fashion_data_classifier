from sqlalchemy import LargeBinary

from fashion_classifier import db,login_manager,app
from flask_login import UserMixin
##password reset
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer




@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))




class User(db.Model,UserMixin):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    date = db.Column(db.Date)
    image_file = db.Column(db.String(20), nullable=False, default='default.png')

    clothing_data = db.relationship('ClothingData', backref='author', lazy=True)

    ##password reset
    ##here we are creating a reset token which will be valid for 30mins to change the password
    def get_reset_token(self,expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id':self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
       s = Serializer(app.config['SECRET_KEY'])
       try:
           user_id = s.loads(token)['user_id']
       except:
           return None
       return User.query.get(user_id)



    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.clothing_data}')"


class ClothingData(db.Model,UserMixin):
    __tablename__ = 'ClothingData'
    id = db.Column(db.Integer, primary_key=True)
    cloth_type = db.Column(db.String(50))
    gender_type = db.Column(db.String(50))
    size_type = db.Column(db.String(50))
    color = db.Column(db.String(50))
    date = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    image_data = db.Column(LargeBinary)
    user_name = db.Column(db.String(20),unique=True, nullable=False)

    tshirt = db.relationship('TSHIRT', backref='author', lazy=True)
    shirts = db.relationship('SHIRT', backref='author', lazy=True)
    pants = db.relationship('PANTS', backref='author', lazy=True)
    shorts = db.relationship('SHORTS', backref='author', lazy=True)
    jackets = db.relationship('JACKETS', backref='author', lazy=True)
    caps = db.relationship('CAPS', backref='author', lazy=True)

    def __repr__(self):
        return f"ClothingData('{self.cloth_type}','{self.gender_type}','{self.size_type}','{self.color}')"



class TSHIRT(db.Model,UserMixin):
    __tablename__ = 'TSHIRT'
    id = db.Column(db.Integer, primary_key=True)
    size = db.Column(db.String(50))
    gender_type = db.Column(db.String(50))
    color = db.Column(db.String(50))
    date = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    image_data = db.Column(LargeBinary)
    user_name = db.Column(db.String(20), db.ForeignKey('ClothingData.user_name'), nullable=False)




    def __repr__(self):
        return f"TSHIRT('{self.gender_type}','{self.size_type}','{self.color}')"

# Define Shirt model
class SHIRT(db.Model,UserMixin):
    __tablename__ = 'SHIRT'
    id = db.Column(db.Integer, primary_key=True)
    size = db.Column(db.String(50))
    gender_type = db.Column(db.String(50))
    color = db.Column(db.String(50))
    date = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    image_data = db.Column(LargeBinary)
    user_name = db.Column(db.String(20), db.ForeignKey('ClothingData.user_name'), nullable=False)




    def __repr__(self):
        return f"SHIRT('{self.gender_type}','{self.size_type}','{self.color}')"


class PANTS(db.Model,UserMixin):
    __tablename__ = 'PANTS'
    id = db.Column(db.Integer, primary_key=True)
    size = db.Column(db.String(50))
    gender_type = db.Column(db.String(50))
    color = db.Column(db.String(50))
    date = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    image_data = db.Column(LargeBinary)
    user_name = db.Column(db.String(20), db.ForeignKey('ClothingData.user_name'), nullable=False)






    def __repr__(self):
        return f"PANTS('{self.gender_type}','{self.size_type}','{self.color}')"

class SHORTS(db.Model,UserMixin):
    __tablename__ = 'SHORTS'
    id = db.Column(db.Integer, primary_key=True)
    size = db.Column(db.String(50))
    gender_type = db.Column(db.String(50))
    color = db.Column(db.String(50))
    date = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    image_data = db.Column(LargeBinary)
    user_name = db.Column(db.String(20), db.ForeignKey('ClothingData.user_name'), nullable=False)






    def __repr__(self):
        return f"SHORTS('{self.gender_type}','{self.size_type}','{self.color}')"

class JACKETS(db.Model,UserMixin):
    __tablename__ = 'JACKETS'
    id = db.Column(db.Integer, primary_key=True)
    size = db.Column(db.String(50))
    gender_type = db.Column(db.String(50))
    color = db.Column(db.String(50))
    date = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    image_data = db.Column(LargeBinary)
    user_name = db.Column(db.String(20), db.ForeignKey('ClothingData.user_name'), nullable=False)







    def __repr__(self):
        return f"JACKETS('{self.gender_type}','{self.size_type}','{self.color}')"

class CAPS(db.Model,UserMixin):
    __tablename__ = 'CAPS'
    id = db.Column(db.Integer, primary_key=True)
    size = db.Column(db.String(50))
    gender_type = db.Column(db.String(50))
    color = db.Column(db.String(50))
    date = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    image_data = db.Column(LargeBinary)
    user_name = db.Column(db.String(20), db.ForeignKey('ClothingData.user_name'), nullable=False)



    def __repr__(self):
        return f"CAPS('{self.gender_type}','{self.size_type}','{self.color}')"





