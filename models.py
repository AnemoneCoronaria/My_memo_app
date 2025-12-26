from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

# 데이터 모델 정의
class Memo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))   # 사용자 참조 추가
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(1000), nullable=False)

    def __repr__(self):
        return f'<Memo {self.title}>'
    
# 유저 데이터 모델
class User(UserMixin, db.Model):
    # __tablename__ = 'Users' 
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(512))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

