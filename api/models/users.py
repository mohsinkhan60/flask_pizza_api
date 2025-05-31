from api.utils import db

class User(db.Model):
   __tablename__ = 'users'

   id = db.Column(db.Integer, primary_key=True)
   username = db.Column(db.String(80), nullable=False)
   email = db.Column(db.String(120), unique=True, nullable=False)
   password_hash = db.Column(db.String(200), nullable=False)
   is_staff = db.Column(db.Boolean(), default=False)
   is_active = db.Column(db.Boolean(), default=True)
   orders = db.relationship('Order', backref='customer', lazy=True)

   def __repr__(self):
       return f'<User {self.username}>'