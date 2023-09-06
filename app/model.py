from app import db, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_gamer(gamer_id):
    return Gamer.query.get(int(gamer_id))

class Gamer(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    gamertag = db.Column(db.String(30), unique=True, nullable=False)
    image = db.Column(db.String(20), nullable=False, default = 'default.jpg')
    password = db.Column(db.String(60),nullable = False)
    posts = db.relationship('Post',backref = 'author', lazy = True)

    def __repr__(self):
        return f"Gamer('{self.gamertag}','{self.password}','{self.image}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100),nullable = False)
    date = db.Column(db.DateTime, nullable= False, default = datetime.utcnow)
    content = db.Column(db.Text,nullable = False)
    image = db.Column(db.String(20))
    gamer_id  = db.Column(db.Integer, db.ForeignKey('gamer.id'),nullable = False)

    def __repr__(self): 
        return f"Gamer('{self.title}','{self.date}')"